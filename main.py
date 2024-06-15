import requests
import json
import config
import pandas as pd
import time
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import tensorflow as tf

MAX_API_CALLS = 100

def extract_tweets(search_query, df, api_calls, reset_token=None):
    base_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {config.BEARER_TOKEN}"
    }
    params = {
        "query": search_query,
        "start_time": "2024-06-11T23:59:59Z",
        "end_time": "2024-06-14T23:59:59Z",
        "max_results": 100,
        "tweet.fields": "lang,text,public_metrics",
        "next_token": reset_token
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.encoding = 'unicode'
        response.raise_for_status() 
        response_json = response.json()
        
        api_calls += 1
        print(f"API call {api_calls} - Status code: {response.status_code}")
        
        # Iterate over response_json to extract the data
        for tweet in response_json["data"]:
            new_row = pd.DataFrame([[tweet["id"], tweet["text"], tweet["lang"], tweet["public_metrics"]["retweet_count"], tweet["public_metrics"]["reply_count"], tweet["public_metrics"]["like_count"], tweet["public_metrics"]["quote_count"], tweet["public_metrics"]["bookmark_count"], tweet["public_metrics"]["impression_count"]]], 
                                        columns=['id', 'text', 'lang', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'bookmark_count', 'impression_count'])
            df = pd.concat([df, new_row], ignore_index=True)

        next_token = response_json.get("meta", {}).get("next_token")
        
        if next_token and api_calls < MAX_API_CALLS:
            print(f"Extracted {len(df)} tweets. Next token: {next_token}")
            extract_tweets(search_query, df, api_calls, next_token)
            
        else:
            print("Completed extracting tweets. Writing to XLSX file...")
            # Create a XSLX file to write the data
            writer = pd.ExcelWriter("bridgerton_tweets.xlsx", engine='openpyxl')

            # Add an empty sheet before writing the DataFrame
            writer.book.create_sheet('Tweets')
    
            # Write the DataFrame to the XLSX file
            df.to_excel(writer, sheet_name='Tweets', index=False)
            
            # Close the XLSX file
            writer.book.save("bridgerton_tweets.xlsx")
            
            # Write the data to a JSON file for faster access for sentiment analysis
            df.to_json("bridgerton_tweets.json", orient="records")
            print("Data written to bridgerton_tweets.xlsx and bridgerton_tweets.json")
            
    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", str(e))
        
        # If the API returns an error of 429 (Rate Limit Exceeded), wait for 15 minutes and try again
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 15 minutes...")
            time.sleep(900)
            extract_tweets(search_query, df, api_calls, reset_token)
            
        else:
            # If the dataframe is not empty, write the data to a XLSX file
            if not df.empty:
                print("Writing to XLSX file...")
                writer = pd.ExcelWriter("bridgerton_tweets.xlsx", engine='openpyxl')
                df.to_excel(writer, sheet_name='Tweets', index=False)
                writer.book.save("bridgerton_tweets.xlsx")
                
                # Write the data to a JSON file for faster access for sentiment analysis
                df.to_json("bridgerton_tweets.json", orient="records")
                print("Data written to bridgerton_tweets.xlsx and bridgerton_tweets.json")
                
            print("Exiting the program...")
        
    except json.JSONDecodeError as e:
        print("Error occurred while decoding JSON response:", str(e))

def sentiment_analysis(tweets_file):
    # Read the JSON file containing the tweets
    with open(tweets_file, 'r') as file:
        tweets = json.load(file)
    
    # Create a DataFrame to store the sentiment analysis data
    df_sentiment = pd.DataFrame(columns=['id', 'text', 'sentiment'])
    
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    
    # Iterate over the tweets and perform sentiment analysis
    for tweet in tweets:
        try:
            text = tweet["text"]
            
            # Remove usernames from the tweet text
            text = re.sub(r'@[A-Za-z0-9]+', '', text)
            
            # Remove URLs from the tweet text
            text = re.sub(r"http\S+", "", text)
            
            # Remove emojis from the tweet text
            emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"  # Dingbats
                            "]+", flags=re.UNICODE)
            emoji_pattern.sub(r'', text)
            
            # Tokenize the tweet text
            tokens = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
            result = model(tokens)
            score = int(torch.argmax(result.logits))+1
            
            if score > 3:
                sentiment = "Positive"
            elif score < 3:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
                
            new_row = pd.DataFrame([[tweet["id"], tweet["text"], sentiment]], columns=['id', 'text', 'sentiment'])
            df_sentiment = pd.concat([df_sentiment, new_row], ignore_index=True)
            
        except Exception as e:
            print("Error occurred while performing sentiment analysis:", str(e))
            
    # Write the sentiment analysis data to a XLSX file
    writer = pd.ExcelWriter("bridgerton_sentiment_analysis.xlsx", engine='openpyxl')
    df_sentiment.to_excel(writer, sheet_name='Sentiment Analysis', index=False)
    writer.book.save("bridgerton_sentiment_analysis.xlsx")
    print("Sentiment analysis data written to bridgerton_sentiment_analysis.xlsx")

def main():
    api_calls = 0
    search_query = "Bridgerton (Michael OR Francesca OR Michaela OR Frannie)"
    
    # Create a DataFrame to store the data
    df = pd.DataFrame(columns=['id', 'text', 'lang', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'bookmark_count', 'impression_count'])

    extract_tweets(search_query, df, api_calls)
    
    # Perform sentiment analysis on the translated tweets
    sentiment_analysis("bridgerton_tweets.json")

if __name__ == "__main__":
    main()