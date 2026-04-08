"""
Raw Data page for SentimentEdge platform
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render(ctx):
    st.title("📋 Raw Data Explorer")

    if not ctx.get("api_key"):
        st.warning("⚠️ Please enter your NewsAPI key in the sidebar to fetch data.")
        return

    st.markdown("### 🔍 Data Browser")

    # Data source selector
    data_source = st.selectbox(
        "Select Data Source",
        ["News Articles", "Sentiment Scores", "Stock Prices", "Correlations", "ML Features"],
        help="Choose which dataset to explore"
    )

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            help="Select date range for data"
        )

    with col2:
        figure_filter = st.text_input(
            "Figure Filter",
            placeholder="e.g., Elon Musk",
            help="Filter by public figure name"
        )

    with col3:
        sentiment_filter = st.slider(
            "Sentiment Range",
            -1.0, 1.0, (-1.0, 1.0),
            help="Filter by sentiment score range"
        )

    # Load and display data
    if st.button("🔄 Load Data", use_container_width=True):
        load_and_display_data(data_source, date_range, figure_filter, sentiment_filter)

def load_and_display_data(source, date_range, figure_filter, sentiment_range):
    with st.spinner(f"Loading {source} data..."):
        # Generate mock data based on source
        if source == "News Articles":
            data = generate_articles_data(date_range, figure_filter, sentiment_range)
        elif source == "Sentiment Scores":
            data = generate_sentiment_data(date_range, figure_filter)
        elif source == "Stock Prices":
            data = generate_stock_data(date_range)
        elif source == "Correlations":
            data = generate_correlation_data(date_range)
        else:  # ML Features
            data = generate_ml_features_data(date_range, figure_filter)

        st.success(f"✅ Loaded {len(data)} records")

        # Data overview
        st.markdown("---")
        st.markdown("### 📊 Data Overview")

        overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)

        with overview_col1:
            st.metric("Total Records", f"{len(data):,}")

        with overview_col2:
            if 'sentiment' in data.columns:
                st.metric("Avg Sentiment", f"{data['sentiment'].mean():.2f}")
            else:
                st.metric("Data Points", f"{len(data):,}")

        with overview_col3:
            if 'date' in data.columns:
                date_span = (data['date'].max() - data['date'].min()).days
                st.metric("Date Span", f"{date_span} days")
            else:
                st.metric("Features", f"{len(data.columns)}")

        with overview_col4:
            st.metric("Last Updated", datetime.now().strftime("%H:%M"))

        # Data table
        st.markdown("### 📋 Raw Data Table")

        # Add search functionality
        search_term = st.text_input("🔍 Search in data", placeholder="Enter search term...")

        if search_term:
            # Simple text search across string columns
            mask = pd.Series(False, index=data.index)
            for col in data.select_dtypes(include=['object']).columns:
                mask |= data[col].astype(str).str.contains(search_term, case=False, na=False)
            filtered_data = data[mask]
        else:
            filtered_data = data

        # Display with pagination
        page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)

        if len(filtered_data) > page_size:
            total_pages = (len(filtered_data) - 1) // page_size + 1
            page = st.slider("Page", 1, total_pages, 1)

            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            display_data = filtered_data.iloc[start_idx:end_idx]
        else:
            display_data = filtered_data

        st.dataframe(display_data, use_container_width=True)

        # Export options
        st.markdown("---")
        st.markdown("### 💾 Export Data")

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            if st.button("📊 Export to CSV", use_container_width=True):
                csv_data = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{source.lower().replace(' ', '_')}_data.csv",
                    mime="text/csv"
                )

        with export_col2:
            if st.button("📈 Export to JSON", use_container_width=True):
                json_data = filtered_data.to_json(orient="records", date_format="iso")
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"{source.lower().replace(' ', '_')}_data.json",
                    mime="application/json"
                )

        with export_col3:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(filtered_data.to_string(), language="text")
                st.success("Data copied to clipboard!")

        # Data statistics
        if len(filtered_data) > 0:
            st.markdown("---")
            st.markdown("### 📈 Data Statistics")

            # Show different stats based on data type
            if 'sentiment' in filtered_data.columns:
                stat_col1, stat_col2, stat_col3 = st.columns(3)

                with stat_col1:
                    st.markdown("**Sentiment Distribution**")
                    fig, ax = plt.subplots(figsize=(4, 3))
                    ax.hist(filtered_data['sentiment'], bins=20, alpha=0.7, color='#00e5a0')
                    ax.set_xlabel('Sentiment Score')
                    ax.set_ylabel('Frequency')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)

                with stat_col2:
                    st.markdown("**Sentiment Over Time**")
                    if 'date' in filtered_data.columns:
                        daily_sentiment = filtered_data.groupby(filtered_data['date'].dt.date)['sentiment'].mean()
                        fig, ax = plt.subplots(figsize=(4, 3))
                        ax.plot(daily_sentiment.index, daily_sentiment.values, marker='o', color='#38bdf8')
                        ax.set_xlabel('Date')
                        ax.set_ylabel('Avg Sentiment')
                        ax.tick_params(axis='x', rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)

                with stat_col3:
                    st.markdown("**Key Statistics**")
                    st.metric("Mean Sentiment", f"{filtered_data['sentiment'].mean():.3f}")
                    st.metric("Sentiment Std", f"{filtered_data['sentiment'].std():.3f}")
                    st.metric("Positive %", f"{(filtered_data['sentiment'] > 0).mean():.1%}")

def generate_articles_data(date_range, figure_filter, sentiment_range):
    """Generate mock news articles data"""
    start_date, end_date = date_range
    days = (end_date - start_date).days + 1

    dates = pd.date_range(start=start_date, end=end_date, freq='h')
    n_articles = min(len(dates), 200)  # Limit for demo

    data = pd.DataFrame({
        'date': dates[:n_articles],
        'title': [f"Article {i+1}: {figure_filter or 'Public Figure'} makes statement" for i in range(n_articles)],
        'content': [f"Full article content {i+1} about market impact..." for i in range(n_articles)],
        'source': np.random.choice(['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'FT'], n_articles),
        'sentiment': np.random.uniform(sentiment_range[0], sentiment_range[1], n_articles),
        'url': [f"https://example.com/article-{i+1}" for i in range(n_articles)]
    })

    return data

def generate_sentiment_data(date_range, figure_filter):
    """Generate mock sentiment analysis data"""
    start_date, end_date = date_range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    data = pd.DataFrame({
        'date': dates,
        'figure': [figure_filter or 'Sample Figure'] * len(dates),
        'compound_score': np.random.normal(0.1, 0.4, len(dates)),
        'positive_score': np.random.uniform(0, 0.8, len(dates)),
        'negative_score': np.random.uniform(0, 0.3, len(dates)),
        'neutral_score': np.random.uniform(0.2, 0.9, len(dates)),
        'article_count': np.random.randint(1, 20, len(dates))
    })

    return data

def generate_stock_data(date_range):
    """Generate mock stock price data"""
    start_date, end_date = date_range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    base_price = 100
    prices = [base_price]
    for i in range(1, len(dates)):
        change = np.random.normal(0, 2)
        prices.append(prices[-1] + change)

    data = pd.DataFrame({
        'date': dates,
        'ticker': ['TSLA'] * len(dates),
        'open': [p + np.random.uniform(-1, 1) for p in prices],
        'high': [p + np.random.uniform(0, 2) for p in prices],
        'low': [p + np.random.uniform(-2, 0) for p in prices],
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, len(dates))
    })

    return data

def generate_correlation_data(date_range):
    """Generate mock correlation analysis data"""
    start_date, end_date = date_range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    figures = ['Elon Musk', 'Jeff Bezos', 'Warren Buffett', 'Cristiano Ronaldo']
    tickers = ['TSLA', 'AMZN', 'BRK.B', 'MANU']

    data = []
    for date in dates:
        for fig, tick in zip(figures, tickers):
            data.append({
                'date': date,
                'figure': fig,
                'ticker': tick,
                'correlation': np.random.uniform(-0.5, 0.8),
                'sentiment_impact': np.random.uniform(0.1, 0.9),
                'confidence': np.random.uniform(0.6, 0.95)
            })

    return pd.DataFrame(data)

def generate_ml_features_data(date_range, figure_filter):
    """Generate mock ML features data"""
    start_date, end_date = date_range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    data = pd.DataFrame({
        'date': dates,
        'figure': [figure_filter or 'Sample Figure'] * len(dates),
        'sentiment_score': np.random.normal(0.1, 0.3, len(dates)),
        'article_volume': np.random.randint(1, 50, len(dates)),
        'source_credibility': np.random.uniform(0.5, 1.0, len(dates)),
        'market_volatility': np.random.uniform(0.1, 0.5, len(dates)),
        'time_of_day': np.random.choice(['morning', 'afternoon', 'evening'], len(dates)),
        'day_of_week': [d.strftime('%A') for d in dates],
        'predicted_impact': np.random.uniform(-5, 5, len(dates))
    })

    return data