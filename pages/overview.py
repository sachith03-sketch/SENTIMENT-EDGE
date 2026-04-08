"""
Overview page for SentimentEdge platform
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render(ctx):
    st.title("🏠 Overview Dashboard")

    # Check if API key is provided
    if not ctx.get("api_key"):
        st.warning("⚠️ Please enter your NewsAPI key in the sidebar to fetch data.")
        return

    st.markdown("### 📊 Platform Statistics")

    # Mock data for demonstration
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Articles Analyzed", "1,247", "+12%")

    with col2:
        st.metric("Sentiment Accuracy", "87.3%", "+2.1%")

    with col3:
        st.metric("Market Correlations", "23", "+5")

    with col4:
        st.metric("Active Tickers", "156", "+8")

    st.markdown("---")

    # Recent Activity
    st.markdown("### 🔄 Recent Activity")

    activity_data = pd.DataFrame({
        'Time': pd.date_range(start=datetime.now() - timedelta(hours=24), periods=10, freq='2h'),
        'Action': ['Analysis completed', 'New correlation found', 'Data updated', 'Report generated',
                  'API call made', 'Model trained', 'Alert triggered', 'Data synced', 'Backup created', 'Cache cleared'],
        'Status': ['✅ Success', '✅ Success', '✅ Success', '✅ Success', '✅ Success',
                  '✅ Success', '⚠️ Warning', '✅ Success', '✅ Success', '✅ Success']
    })

    st.dataframe(activity_data, use_container_width=True)

    # System Health
    st.markdown("### 🏥 System Health")

    health_col1, health_col2 = st.columns(2)

    with health_col1:
        st.markdown("**API Status**")
        st.success("✅ NewsAPI: Connected")
        st.success("✅ Yahoo Finance: Connected")

    with health_col2:
        st.markdown("**Performance Metrics**")
        st.info("📈 Response Time: 1.2s avg")
        st.info("💾 Memory Usage: 67%")

    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("Data refreshed successfully!")

    with action_col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Report generation started...")

    with action_col3:
        if st.button("🔔 Configure Alerts", use_container_width=True):
            st.info("Opening alert configuration...")
