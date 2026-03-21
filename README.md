# 📈 SentimentEdge - Financial Sentiment Analysis Platform

A sophisticated web application that analyzes the sentiment of news articles about influential public figures and correlates it with stock market performance. Built with Streamlit, this platform provides real-time insights into how public statements impact financial markets.

## 🌟 Features

### 🏠 **Overview Dashboard**
- Real-time platform statistics and metrics
- Recent activity monitoring
- System health status
- Quick action buttons for common tasks

### 🔍 **Single Figure Analysis**
- Individual sentiment analysis for public figures
- Stock price correlation analysis
- Interactive sentiment trend visualizations
- Top articles with sentiment scoring

### ⚖️ **Comparison Engine**
- Side-by-side comparison of multiple figures
- Statistical analysis and insights
- Combined trend visualization
- Performance recommendations

### 🤖 **ML Predictions**
- Machine learning model training interface
- Feature importance analysis
- Future sentiment and price predictions
- Model performance metrics and evaluation

### 📋 **Raw Data Explorer**
- Comprehensive data browser for all datasets
- Advanced filtering and search capabilities
- Export functionality (CSV/JSON)
- Statistical analysis and visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- NewsAPI key (free at [newsapi.org](https://newsapi.org))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sentiment-edge.git
   cd sentiment-edge
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

6. **Enter your NewsAPI key** in the sidebar to start analyzing data

## 📊 Technical Architecture

### Core Technologies
- **Frontend:** Streamlit with custom CSS styling
- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn
- **Sentiment Analysis:** VADER (NLTK)
- **Financial Data:** yfinance
- **News Aggregation:** NewsAPI

### Project Structure
```
sentiment-edge/
├── app.py                 # Main Streamlit application
├── pages/                 # Page modules
│   ├── overview.py       # Overview dashboard
│   ├── single.py         # Single figure analysis
│   ├── comparison.py     # Comparison engine
│   ├── ml.py            # ML predictions
│   └── raw_data.py      # Data explorer
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

### API Keys
- **NewsAPI:** Get your free API key at [newsapi.org](https://newsapi.org)
- The application will prompt for the API key in the sidebar

### Customization
- Modify `app.py` for UI theme changes
- Update page modules in the `pages/` directory for functionality changes
- Adjust analysis parameters in individual page modules

## 📈 Usage Examples

### Analyzing a Single Figure
1. Navigate to "🔍 Single Figure Analysis"
2. Enter a public figure name (e.g., "Elon Musk")
3. Enter associated stock ticker (e.g., "TSLA")
4. Click "🚀 Run Analysis"
5. View sentiment trends, correlations, and top articles

### Comparing Multiple Figures
1. Go to "⚖️ Comparison Engine"
2. Enter two figure names and their tickers
3. Set analysis parameters
4. Click "⚖️ Compare Figures"
5. Analyze comparative statistics and trends

### ML Predictions
1. Select "🤖 ML Predictions"
2. Choose a prediction model type
3. Configure features and parameters
4. Click "🚀 Train & Predict"
5. Review model performance and future predictions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NewsAPI** for news data aggregation
- **Yahoo Finance** for financial data
- **VADER Sentiment** for sentiment analysis
- **Streamlit** for the web framework

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the code comments for implementation details

---

**Built with ❤️ for financial sentiment analysis**