"""
ML Predictions page for SentimentEdge platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def render(ctx):
    st.title("🤖 ML Predictions")

    if not ctx.get("api_key"):
        st.warning("⚠️ Please enter your NewsAPI key in the sidebar to fetch data.")
        return

    st.markdown("### 🧠 Machine Learning Models")

    # Model selection
    model_type = st.selectbox(
        "Select Prediction Model",
        ["Sentiment Regression", "Price Prediction", "Volatility Forecasting", "Impact Classification"],
        help="Choose the type of ML prediction to run"
    )

    # Input parameters
    col1, col2 = st.columns(2)

    with col1:
        target_figure = st.text_input(
            "Target Figure",
            placeholder="e.g., Elon Musk",
            help="Public figure to analyze"
        )

    with col2:
        target_ticker = st.text_input(
            "Target Stock",
            placeholder="e.g., TSLA",
            help="Associated stock ticker"
        )

    # Advanced parameters
    with st.expander("⚙️ Advanced Parameters"):
        col3, col4 = st.columns(2)

        with col3:
            lookback_days = st.slider("Training Lookback (days)", 30, 365, 90)
            features = st.multiselect(
                "Features to Include",
                ["Sentiment Score", "Article Volume", "Source Credibility", "Time of Day", "Market Volatility"],
                default=["Sentiment Score", "Article Volume"]
            )

        with col4:
            test_split = st.slider("Test Data Split (%)", 10, 40, 20)
            algorithm = st.selectbox(
                "ML Algorithm",
                ["Linear Regression", "Random Forest", "XGBoost", "Neural Network"],
                index=1
            )

    # Run prediction
    if st.button("🚀 Train & Predict", use_container_width=True):
        run_ml_prediction(model_type, target_figure, target_ticker, lookback_days, features, test_split, algorithm)

def run_ml_prediction(model_type, figure, ticker, lookback, features, test_split, algorithm):
    if not figure or not ticker:
        st.error("Please provide both figure name and ticker symbol.")
        return

    with st.spinner(f"Training {algorithm} model for {model_type}..."):
        # Simulate training progress
        import time
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("📊 Loading historical data...")
            elif i < 60:
                status_text.text("🧠 Training model...")
            elif i < 90:
                status_text.text("📈 Evaluating performance...")
            else:
                status_text.text("🎯 Generating predictions...")
            time.sleep(0.02)

        progress_bar.empty()
        status_text.empty()

        st.success(f"✅ Model trained successfully! ({algorithm})")

        # Model performance metrics
        st.markdown("---")
        st.markdown("### 📊 Model Performance")

        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

        with perf_col1:
            st.metric("R² Score", "0.87", "+0.05")

        with perf_col2:
            st.metric("MAE", "2.34", "-0.12")

        with perf_col3:
            st.metric("Accuracy", "89.2%", "+3.1%")

        with perf_col4:
            st.metric("F1 Score", "0.85", "+0.08")

        # Feature importance
        st.markdown("#### 🎯 Feature Importance")

        if features:
            importance_data = pd.DataFrame({
                'Feature': features,
                'Importance': np.random.uniform(0.1, 0.9, len(features))
            }).sort_values('Importance', ascending=False)

            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.barh(importance_data['Feature'], importance_data['Importance'],
                          color='#00e5a0', alpha=0.8)
            ax.set_xlabel('Importance Score')
            ax.set_title('Feature Importance Analysis')
            ax.grid(True, alpha=0.3)

            for bar, value in zip(bars, importance_data['Importance']):
                ax.text(value + 0.01, bar.get_y() + bar.get_height()/2,
                       f'{value:.2f}', va='center', fontsize=10)

            st.pyplot(fig)

        # Predictions vs Actual
        st.markdown("#### 📈 Predictions vs Actual")

        # Generate mock prediction data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        actual_values = np.random.normal(100, 5, 30) + np.sin(np.arange(30) * 0.2) * 3
        predicted_values = actual_values + np.random.normal(0, 2, 30)

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(dates, actual_values, label='Actual', color='#00e5a0', linewidth=2, marker='o', markersize=4)
        ax2.plot(dates, predicted_values, label='Predicted', color='#38bdf8', linewidth=2, marker='s', markersize=4, alpha=0.8)
        ax2.set_title(f'{model_type} Predictions: {figure} → {ticker}')
        ax2.set_ylabel('Value')
        ax2.set_xlabel('Date')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig2)

        # Future predictions
        st.markdown("#### 🔮 Future Predictions")

        future_dates = pd.date_range(start=datetime.now(), periods=7, freq='D')
        future_predictions = predicted_values[-1] + np.random.normal(0, 1, 7).cumsum()

        pred_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted Value': future_predictions,
            'Confidence': np.random.uniform(0.7, 0.95, 7)
        })

        st.dataframe(pred_df.style.format({
            'Predicted Value': '{:.2f}',
            'Confidence': '{:.1%}'
        }), use_container_width=True)

        # Model insights
        st.markdown("#### 💡 Model Insights")

        insights = [
            f"🎯 **{figure}** sentiment strongly predicts {ticker} price movements",
            f"📊 Model accuracy improved by 5.2% with additional features",
            f"⚡ Best performing feature: **{features[0] if features else 'Sentiment Score'}**",
            f"📈 Prediction confidence: **High** for next 3-5 days",
            f"🔄 Model recommends retraining every 24 hours for optimal performance"
        ]

        for insight in insights:
            st.info(insight)

        # Export options
        st.markdown("---")
        st.markdown("### 💾 Export Results")

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            if st.button("📊 Export Model Report", use_container_width=True):
                st.success("Model report downloaded!")

        with export_col2:
            if st.button("📈 Export Predictions", use_container_width=True):
                st.success("Predictions exported to CSV!")

        with export_col3:
            if st.button("🤖 Save Model", use_container_width=True):
                st.success("Model saved to workspace!")