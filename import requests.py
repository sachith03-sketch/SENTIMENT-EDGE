import requests
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import yfinance as yf

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)

# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
API_KEY   = '7a6b9cb44123404bbed4676dd31c04fa'
QUERY     = 'Cristiano Ronaldo'
TICKER    = 'MANU'          # Manchester United — linked to Ronaldo news
PAGE_SIZE = 20

# ── 2. FETCH NEWS ARTICLES ────────────────────────────────────────────────────
url = (
    f'https://newsapi.org/v2/everything'
    f'?q={QUERY}&language=en&sortBy=publishedAt'
    f'&pageSize={PAGE_SIZE}&apiKey={API_KEY}'
)

response = requests.get(url)
response.raise_for_status()                     # surface HTTP errors clearly
data     = response.json()
articles = data.get('articles', [])

if not articles:
    raise ValueError("No articles returned. Check your API key or query.")

# ── 3. EXTRACT TEXT AND DATE ──────────────────────────────────────────────────
records = []
for article in articles:
    text = article.get('description') or article.get('title') or ''
    date = article.get('publishedAt', '')[:10]
    if text and date:
        records.append({'text': text, 'date': date})

df = pd.DataFrame(records)
df['date'] = pd.to_datetime(df['date'])

# ── 4. SENTIMENT ANALYSIS (VADER) ────────────────────────────────────────────
sia = SentimentIntensityAnalyzer()

df['compound']  = df['text'].apply(lambda t: sia.polarity_scores(t)['compound'])
df['positive']  = df['text'].apply(lambda t: sia.polarity_scores(t)['pos'])
df['negative']  = df['text'].apply(lambda t: sia.polarity_scores(t)['neg'])
df['neutral']   = df['text'].apply(lambda t: sia.polarity_scores(t)['neu'])

# Daily average compound sentiment
daily_sentiment = df.groupby('date')['compound'].mean()

if daily_sentiment.empty:
    raise ValueError("No dated sentiment data available to proceed.")

# ── 5. FETCH STOCK DATA ───────────────────────────────────────────────────────
start_date = daily_sentiment.index.min().strftime('%Y-%m-%d')
end_date   = (daily_sentiment.index.max() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

stock_data = yf.download(TICKER, start=start_date, end=end_date,
                          interval='1d', auto_adjust=True)

if stock_data.empty:
    raise ValueError(f"No stock data returned for ticker '{TICKER}'.")

# Use 'Close' (auto_adjust=True already adjusts it)
stock_prices = stock_data['Close']
if isinstance(stock_prices, pd.Series):
    stock_prices.index = stock_prices.index.normalize()

# ── 6. MERGE SENTIMENT + STOCK ────────────────────────────────────────────────
if isinstance(stock_prices, pd.Series) and not stock_prices.empty:
    combined = pd.merge(
        daily_sentiment.rename('sentiment'),
        stock_prices.rename('stock'),
        left_index=True,
        right_index=True,
        how='inner'
    )
else:
    combined = pd.DataFrame()  # empty dataframe

if combined.empty:
    print("⚠ No overlapping dates between sentiment and stock data.")
    print("  Sentiment dates:", daily_sentiment.index.tolist())
    print("  Stock dates    :", stock_prices.index.tolist())
else:
    correlation = combined['sentiment'].corr(combined['stock'])
    print(f"\nPearson Correlation (sentiment vs. stock price): {correlation:.4f}")

# ── 7. VISUALISATIONS ─────────────────────────────────────────────────────────
sns.set_theme(style='darkgrid')

# --- Plot 1: Per-article sentiment scores ------------------------------------
fig1, ax = plt.subplots(figsize=(12, 5))
colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in df['compound']]
ax.bar(df.index, df['compound'], color=colors, edgecolor='white', linewidth=0.5)
ax.axhline(0, color='white', linewidth=0.8, linestyle='--')
ax.set_title(f'Per-Article Sentiment Score — "{QUERY}"', fontsize=14, fontweight='bold')
ax.set_xlabel('Article Index')
ax.set_ylabel('VADER Compound Score')
plt.tight_layout()
plt.savefig('plot1_article_sentiment.png', dpi=150)
plt.show()

# --- Plot 2: Daily average sentiment -----------------------------------------
fig2, ax = plt.subplots(figsize=(12, 5))
ax.bar(daily_sentiment.index, daily_sentiment.values,
       color=['#2ecc71' if v >= 0 else '#e74c3c' for v in daily_sentiment.values],
       width=0.6, edgecolor='white')
ax.axhline(0, color='grey', linewidth=0.8, linestyle='--')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig2.autofmt_xdate()
ax.set_title('Daily Average Sentiment Score', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Mean Compound Score')
plt.tight_layout()
plt.savefig('plot2_daily_sentiment.png', dpi=150)
plt.show()

# --- Plot 3: Dual-axis sentiment vs. stock price (only if data overlaps) -----
if not combined.empty:
    fig3, ax1 = plt.subplots(figsize=(13, 6))
    ax2 = ax1.twinx()

    ax1.plot(combined.index, combined['sentiment'],
             color='#2ecc71', linewidth=2, marker='o', markersize=5,
             label='Sentiment (compound)')
    ax1.axhline(0, color='#2ecc71', linewidth=0.6, linestyle='--', alpha=0.5)
    ax1.set_ylabel('Sentiment Score', color='#2ecc71', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#2ecc71')

    ax2.plot(combined.index, combined['stock'],
             color='#3498db', linewidth=2, marker='s', markersize=5,
             label=f'{TICKER} Close Price')
    ax2.set_ylabel(f'{TICKER} Stock Price (USD)', color='#3498db', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='#3498db')

    # Shared legend
    lines  = ax1.get_lines() + ax2.get_lines()
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig3.autofmt_xdate()
    ax1.set_title(
        f'Sentiment vs. {TICKER} Stock Price\n'
        f'Pearson r = {correlation:.4f}',
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig('plot3_sentiment_vs_stock.png', dpi=150)
    plt.show()

# --- Plot 4: Sentiment component breakdown -----------------------------------
fig4, ax = plt.subplots(figsize=(12, 5))
ax.stackplot(
    df.index,
    df['positive'], df['neutral'], df['negative'],
    labels=['Positive', 'Neutral', 'Negative'],
    colors=['#2ecc71', '#95a5a6', '#e74c3c'],
    alpha=0.8
)
ax.set_title('Sentiment Component Breakdown per Article', fontsize=14, fontweight='bold')
ax.set_xlabel('Article Index')
ax.set_ylabel('Score Proportion')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('plot4_sentiment_breakdown.png', dpi=150)
plt.show()

print("\n✅ All plots saved successfully!")
print(df[['date', 'compound', 'text']].sort_values('date').to_string(index=False))