import requests
import json
import config
import pandas as pd

MAX_API_CALLS = 1

def extract_tweets(search_query, reset_token=None):
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
    
    api_calls = 0
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.encoding = 'unicode'
        response.raise_for_status() 
        response_json = response.json()
        print(response_json)
        
        api_calls += 1

        with open("tweets.json", "a") as file:
            json.dump(response_json["data"], file)
            file.write("\n")

        next_token = response_json.get("meta", {}).get("next_token")
        
        if next_token and api_calls < MAX_API_CALLS:
            extract_tweets(search_query, next_token)
            
    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", str(e))
        
    except json.JSONDecodeError as e:
        print("Error occurred while decoding JSON response:", str(e))

def main():
    search_query = "Bridgerton (Michael OR Francesca OR Michaela OR Frannie)"
    extract_tweets(search_query)

    # Create a XSLX file to write the data
    writer = pd.ExcelWriter("bridgerton_tweets.xlsx", engine='openpyxl')

    # Add an empty sheet before writing the DataFrame
    writer.book.create_sheet('Tweets')

    # Read the `tweets.json` file
    with open("tweets.json", "r") as file:
        for line in file:
            data = json.loads(line)
            
            # Create a DataFrame to store the data
            df = pd.DataFrame(columns=['id', 'text', 'lang', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'bookmark_count', 'impression_count'])
            
            # Loop through each tweet in the data
            for tweet in data['data']:
                tweet_id = tweet['id']
                tweet_text = tweet['text'].replace('\n', ' ')
                tweet_lang = tweet['lang']
                tweet_retweet_count =  tweet['public_metrics']['retweet_count']
                tweet_reply_count =  tweet['public_metrics']['reply_count']
                tweet_like_count =  tweet['public_metrics']['like_count']
                tweet_quote_count =  tweet['public_metrics']['quote_count']
                tweet_bookmark_count =  tweet['public_metrics']['bookmark_count']
                tweet_impression_count =  tweet['public_metrics']['impression_count']

                # Append the information to the DataFrame
                df = pd.concat([df, pd.DataFrame([[tweet_id, tweet_text, tweet_lang, tweet_retweet_count, tweet_reply_count, tweet_like_count, tweet_quote_count, tweet_bookmark_count, tweet_impression_count]], columns=df.columns)], ignore_index=True)
        
            # Write the DataFrame to the XLSX file
            df.to_excel(writer, sheet_name='Tweets', index=False)

if __name__ == "__main__":
    main()