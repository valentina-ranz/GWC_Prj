import requests
from textblob import TextBlob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Function to fetch and process news articles
def fetch_and_analyze_news():
    # Prompt user for search keyword
    keyword = input("Enter the topic you want to analyze (e.g., election, immigration): ").strip()

    # API configuration
    api_key = 'cce24217ccbc489896b1e80021bd16d6'
    url = 'https://newsapi.org/v2/everything'

    # Parameters for API request
    params = {
        'q': keyword,
        'apiKey': api_key,
        'language': 'en',
        'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'sortBy': 'relevancy',
    }

    # Fetch news articles
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # Collect sentiment data
    sentiments = []
    titles = []
    urls = []

    for article in data.get('articles', []):
        title = article['title']
        description = article.get('description', '')
        content = article.get('content', '')

        # Analyze sentiment
        full_text = f"{title}. {description} {content}"
        blob = TextBlob(full_text)
        polarity = blob.sentiment.polarity

        # Categorize sentiment
        sentiment_category = (
            'Positive' if polarity > 0 else
            'Negative' if polarity < 0 else 'Neutral'
        )

        # Store data for visualization
        sentiments.append(sentiment_category)
        titles.append(title)
        urls.append(article['url'])

    # Create a DataFrame for analysis
    df = pd.DataFrame({'Title': titles, 'URL': urls, 'Sentiment': sentiments})

    # Save the data to a CSV file
    csv_filename = f'{keyword}_sentiment_analysis.csv'
    df.to_csv(csv_filename, index=False)

    print(f"Sentiment analysis completed and saved to '{csv_filename}'.")

    # Plot 1: Bar chart of sentiment counts
    plt.figure(figsize=(8, 5))
    df['Sentiment'].value_counts().plot(kind='bar')
    plt.title(f'Distribution of Sentiments in {keyword.capitalize()} Articles')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

    # Plot 2: Pie chart of sentiment proportions
    plt.figure(figsize=(6, 6))
    df['Sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title(f'Proportion of Sentiments in {keyword.capitalize()} Articles')
    plt.ylabel('')  # Hide y-label for aesthetics
    plt.show()

    # Plot 3: Word Cloud for article content
    all_text = ' '.join(
        [f"{title}. {description} {content}" for title, description, content in zip(titles, df['Title'], urls)]
    )
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide axes for cleaner look
    plt.title(f'Word Cloud for {keyword.capitalize()} Articles')
    plt.show()

# Run the function
if __name__ == "__main__":
    fetch_and_analyze_news()
