# Cybersecurity-News-Dashboard

## Features 

- Fetch news from multiple RSS feeds 
- Sentiment analysis of news articles 
- Keyword extraction from news articles 
- Display trending topics - Pagination for news articles 
- Visualization of the number of articles per source 
- RSS feed management (add/remove feeds)

## Requirements

 - Python 3.12 
 - Streamlit 
 - Feedparser 
 - Pandas 
 - Matplotlib 
 - TextBlob


## Installation 

### Running Locally

1. Clone the repository: 

``` git clone https://github.com/sivolko/cybersecurity-news-dashboard.git 
  cd cybersecurity-news-dashboard
 ``` 
2. 

Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run app.py
```

Running with Docker 

1. Build the Docker Image:
```
docker build -t sivolko/cybersecurity-news-dashboard:latest .
```
2. Run the Docker Container:
```
docker run -p 8501:8501 sivolko/cybersecurity-news-dashboard:latest

```
3. Open your browser and go to http://localhost:8501 to access the app.

4. Directly Pull Image from Docker Hub
   ```
    docker pull sivolko/cybersecurity-news-dashboard
   ```
   ![image](https://github.com/user-attachments/assets/44057396-1c3a-425d-a772-202861ef8460)
