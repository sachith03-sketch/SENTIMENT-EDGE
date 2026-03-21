"""
Single Figure Analysis page for SentimentEdge platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def render(ctx):
    st.title("🔍 Single Figure Analysis")

    if not ctx.get("api_key"):
        st.warning("⚠️ Please enter your NewsAPI key in the sidebar to fetch data.")
        return

    # Input section
    st.markdown("### 🎯 Analysis Configuration")

    col1, col2 = st.columns([2, 1])

    with col1:
        figure_name = st.text_input(
            "Figure Name",
            placeholder="e.g., Cristiano Ronaldo, Elon Musk, Warren Buffett",
            help="Enter the name of the public figure to analyze"
        )

    with col2:
        ticker = st.text_input(
            "Stock Ticker",
            placeholder="e.g., TSLA, AAPL, GOOGL",
            help="Associated stock ticker symbol"
        )

    # Analysis parameters
    col3, col4, col5 = st.columns(3)

    with col3:
        days_back = st.slider("Days to Analyze", 1, 30, 7)

    with col4:
        sentiment_threshold = st.slider("Sentiment Threshold", -1.0, 1.0, 0.0, 0.1)

    with col5:
        if st.button("🚀 Run Analysis", use_container_width=True):
            run_analysis(figure_name, ticker, days_back, sentiment_threshold)

def run_analysis(figure_name, ticker, days_back, sentiment_threshold):
    if not figure_name or not ticker:
        st.error("Please provide both figure name and ticker symbol.")
        return

    with st.spinner("Analyzing sentiment and market data..."):
        # Mock analysis results
        st.success(f"✅ Analysis completed for {figure_name} ({ticker})")

        # Results section
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")

        # Key metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric("Articles Found", "47", "+12")

        with metric_col2:
            st.metric("Avg Sentiment", "0.23", "+0.05")

        with metric_col3:
            st.metric("Correlation", "0.67", "+0.12")

        with metric_col4:
            st.metric("Confidence", "89%", "+5%")

        # Sentiment over time chart
        st.markdown("#### 📈 Sentiment Trend")

        # Generate mock data
        dates = pd.date_range(start=datetime.now() - timedelta(days=days_back), periods=days_back, freq='D')
        sentiment_scores = np.random.normal(0.2, 0.3, days_back)
        sentiment_scores = np.clip(sentiment_scores, -1, 1)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(dates, sentiment_scores, marker='o', linewidth=2, color='#00e5a0')
        ax.axhline(y=0, color='white', linestyle='--', alpha=0.5)
        ax.set_title(f'Sentiment Analysis: {figure_name}')
        ax.set_ylabel('Sentiment Score')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # Top articles
        st.markdown("#### 📰 Top Articles")

        articles_data = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now() - timedelta(days=3), periods=5, freq='D'),
            'Title': [
                f'{figure_name} announces major investment in {ticker}',
                f'Analysis: How {figure_name} influences market sentiment',
                f'{figure_name} comments spark trading activity',
                f'Breaking: {figure_name} partners with tech giant',
                f'{figure_name} reveals new business strategy'
            ],
            'Sentiment': [0.8, 0.6, -0.2, 0.9, 0.4],
            'Source': ['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'FT']
        })

        # Color code sentiment
        def color_sentiment(val):
            color = '#00e5a0' if val > 0.1 else '#ff4d6d' if val < -0.1 else '#f59e0b'
            return f'color: {color}'

        st.dataframe(
            articles_data.style.applymap(color_sentiment, subset=['Sentiment']),
            use_container_width=True
        )

        # Market correlation
        st.markdown("#### 📊 Market Correlation")

        corr_col1, corr_col2 = st.columns(2)

        with corr_col1:
            st.markdown("**Sentiment vs Stock Price**")
            correlation = 0.67
            st.metric("Pearson Correlation", f"{correlation:.2f}")

            if correlation > 0.5:
                st.success("Strong positive correlation detected!")
            elif correlation > 0.2:
                st.info("Moderate positive correlation")
            else:
                st.warning("Weak or no correlation")

        with corr_col2:
            # Mock correlation scatter plot
            sentiment_vals = np.random.normal(0.2, 0.3, 50)
            stock_vals = sentiment_vals * 0.6 + np.random.normal(0, 0.2, 50) + 100

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.scatter(sentiment_vals, stock_vals, alpha=0.6, color='#00e5a0')
            ax2.set_xlabel('Sentiment Score')
            ax2.set_ylabel(f'{ticker} Stock Price')
            ax2.set_title('Sentiment vs Price Correlation')
            ax2.grid(True, alpha=0.3)

            st.pyplot(fig2)