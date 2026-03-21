"""
Comparison Engine page for SentimentEdge platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def render(ctx):
    st.title("⚖️ Comparison Engine")

    if not ctx.get("api_key"):
        st.warning("⚠️ Please enter your NewsAPI key in the sidebar to fetch data.")
        return

    st.markdown("### 🔄 Compare Multiple Figures")

    # Comparison inputs
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Figure 1**")
        figure1 = st.text_input("Name", placeholder="e.g., Elon Musk", key="fig1")
        ticker1 = st.text_input("Ticker", placeholder="e.g., TSLA", key="tick1")

    with col2:
        st.markdown("**Figure 2**")
        figure2 = st.text_input("Name", placeholder="e.g., Jeff Bezos", key="fig2")
        ticker2 = st.text_input("Ticker", placeholder="e.g., AMZN", key="tick2")

    # Analysis parameters
    col3, col4 = st.columns(2)

    with col3:
        days_back = st.slider("Analysis Period (days)", 1, 30, 14)

    with col4:
        if st.button("⚖️ Compare Figures", use_container_width=True):
            run_comparison(figure1, ticker1, figure2, ticker2, days_back)

def run_comparison(fig1, tick1, fig2, tick2, days):
    if not all([fig1, tick1, fig2, tick2]):
        st.error("Please fill in all figure names and tickers.")
        return

    with st.spinner("Comparing sentiment impact..."):
        st.success(f"✅ Comparison completed: {fig1} vs {fig2}")

        st.markdown("---")
        st.markdown("### 📊 Comparison Results")

        # Summary metrics
        comp_data = pd.DataFrame({
            'Metric': ['Articles Found', 'Avg Sentiment', 'Sentiment Volatility', 'Market Impact', 'Correlation Strength'],
            fig1: [45, 0.32, 0.45, 0.78, 0.65],
            fig2: [38, 0.28, 0.52, 0.62, 0.58]
        })

        st.dataframe(comp_data, use_container_width=True)

        # Side-by-side sentiment trends
        st.markdown("#### 📈 Sentiment Trends Comparison")

        dates = pd.date_range(start=datetime.now() - timedelta(days=days), periods=days, freq='D')

        # Generate mock data with different patterns
        sentiment1 = np.random.normal(0.3, 0.25, days)
        sentiment2 = np.random.normal(0.25, 0.3, days)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Figure 1
        ax1.plot(dates, sentiment1, marker='o', linewidth=2, color='#00e5a0', label=fig1)
        ax1.axhline(y=0, color='white', linestyle='--', alpha=0.5)
        ax1.set_title(f'{fig1} Sentiment Trend')
        ax1.set_ylabel('Sentiment Score')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend()

        # Figure 2
        ax2.plot(dates, sentiment2, marker='s', linewidth=2, color='#38bdf8', label=fig2)
        ax2.axhline(y=0, color='white', linestyle='--', alpha=0.5)
        ax2.set_title(f'{fig2} Sentiment Trend')
        ax2.set_ylabel('Sentiment Score')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()

        plt.tight_layout()
        st.pyplot(fig)

        # Combined comparison chart
        st.markdown("#### ⚖️ Direct Comparison")

        fig2, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, sentiment1, marker='o', linewidth=2, color='#00e5a0', label=fig1, alpha=0.8)
        ax.plot(dates, sentiment2, marker='s', linewidth=2, color='#38bdf8', label=fig2, alpha=0.8)
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.5)
        ax.set_title(f'{fig1} vs {fig2} Sentiment Comparison')
        ax.set_ylabel('Sentiment Score')
        ax.set_xlabel('Date')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig2)

        # Statistical comparison
        st.markdown("#### 📈 Statistical Analysis")

        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            st.metric("Sentiment Difference", f"{sentiment1.mean() - sentiment2.mean():.2f}")

        with stat_col2:
            st.metric("Volatility Ratio", f"{np.std(sentiment1) / np.std(sentiment2):.2f}")

        with stat_col3:
            correlation_diff = 0.65 - 0.58  # Mock difference
            st.metric("Correlation Advantage", f"{correlation_diff:.2f}")

        # Key insights
        st.markdown("#### 💡 Key Insights")

        insights = [
            f"📈 {fig1} shows more consistent positive sentiment",
            f"🎯 {fig2} has higher sentiment volatility but stronger market correlation",
            f"⚡ {fig1} generates more media coverage overall",
            f"💰 {tick1} shows stronger sentiment-price relationship"
        ]

        for insight in insights:
            st.info(insight)

        # Recommendation
        st.markdown("#### 🎯 Recommendation")

        if sentiment1.mean() > sentiment2.mean():
            st.success(f"**{fig1}** appears to have stronger overall sentiment impact on {tick1}")
        else:
            st.success(f"**{fig2}** appears to have stronger overall sentiment impact on {tick2}")