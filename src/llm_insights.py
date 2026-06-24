"""
Optional Groq LLM insight generator for Executive Overview.
Uses Streamlit secrets for API key and falls back gracefully when unavailable.
"""

import json
from typing import Optional

import pandas as pd
import requests
import streamlit as st


def get_groq_api_key() -> Optional[str]:
    """Read Groq API key from .streamlit/secrets.toml."""
    try:
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


def build_executive_context(df_latest: pd.DataFrame) -> dict:
    """Build compact, factual context for LLM prompt."""
    total_sales = float(df_latest["sales"].sum())
    avg_score = float(df_latest["market_shift_score"].mean())
    median_growth = float(df_latest["sales_growth_rate"].median() * 100)

    category_summary = (
        df_latest.groupby("category")
        .agg(
            total_sales=("sales", "sum"),
            avg_score=("market_shift_score", "mean"),
            avg_growth=("sales_growth_rate", "mean"),
        )
        .reset_index()
        .sort_values("avg_score", ascending=False)
    )
    category_summary["avg_growth"] = category_summary["avg_growth"] * 100

    top_positive = df_latest.nlargest(5, "market_shift_score")[
        ["product_name", "category", "region", "market_shift_score", "sales_growth_rate", "signal"]
    ].copy()
    top_positive["sales_growth_rate"] = top_positive["sales_growth_rate"] * 100

    top_decline = df_latest.nsmallest(5, "market_shift_score")[
        ["product_name", "category", "region", "market_shift_score", "sales_growth_rate", "signal"]
    ].copy()
    top_decline["sales_growth_rate"] = top_decline["sales_growth_rate"] * 100

    signal_counts = df_latest["signal"].value_counts().to_dict()

    return {
        "total_sales": round(total_sales, 2),
        "avg_market_shift_score": round(avg_score, 2),
        "median_growth_rate_pct": round(median_growth, 2),
        "signal_counts": signal_counts,
        "category_summary": category_summary.round(2).to_dict(orient="records"),
        "top_positive_signals": top_positive.round(2).to_dict(orient="records"),
        "top_decline_warnings": top_decline.round(2).to_dict(orient="records"),
    }


def generate_ai_executive_brief(df_latest: pd.DataFrame, model: str = "llama-3.1-8b-instant") -> str:
    """
    Generate AI executive brief using Groq Chat Completions API.
    Returns fallback guidance if API key is missing.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return (
            "**AI Executive Brief belum aktif.**\n\n"
            "Tambahkan `GROQ_API_KEY` di `.streamlit/secrets.toml`, lalu refresh dashboard. "
            "Sementara ini, gunakan Executive Summary rule-based di bawah halaman."
        )

    context = build_executive_context(df_latest)

    system_prompt = """
You are a senior FMCG business analyst. Generate a concise executive brief from provided metrics only.
Rules:
- Use only provided data. Do not invent causes.
- Do not mention competitors, pricing, promotion, distribution, macro factors, or customer behavior unless explicitly provided.
- Use cautious business language: may indicate, shows early signal, should be monitored, requires validation.
- Do not overclaim prediction or causality.
- Output in English.
- Maximum 140 words.
- Format with: 1 short paragraph + 3 bullet action points.
""".strip()

    user_prompt = f"""
Create an executive brief for this FMCG Market Shift dashboard.

Data context JSON:
{json.dumps(context, indent=2)}
""".strip()

    try:
        groq_model = st.secrets.get("GROQ_MODEL", model)
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": groq_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 260,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return (
            "**AI Executive Brief gagal dibuat.**\n\n"
            f"Error: `{exc}`\n\n"
            "Periksa API key, koneksi internet, atau model yang digunakan."
        )
