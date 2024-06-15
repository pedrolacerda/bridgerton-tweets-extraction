import json
import glob
import pandas as pd

# Get a list of all JSON files matching the pattern
json_files = glob.glob('tweets/tweets_*.json')

# Create a XSLX file to write the data
writer = pd.ExcelWriter("bridgerton_tweets.xlsx", engine='openpyxl')

# Add an empty sheet before writing the DataFrame
writer.book.create_sheet('Tweets')

# Create a DataFrame to store the data
df = pd.DataFrame(columns=['id', 'text', 'lang', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'bookmark_count', 'impression_count'])

# Loop through each JSON file
for file in json_files:
    """
    The root object of interest is "data" which is a list of tweets. Each tweet is a dictionary with the following keys
    - id: The unique identifier of the tweet
    - text: The text content of the tweet
    - lang: The language of the tweet
    - public_metrics: A dictionary containing the public metrics of the tweet
        - retweet_count: The number of retweets of the tweet
        - reply_count: The number of replies to the tweet
        - like_count: The number of likes of the tweet
        - quote_count: The number of quotes of the tweet
        - bookmark_count: The number of bookmarks of the tweet
        - impression_count: The number of impressions of the tweet
    """
    
    # Open the JSON file and load the data
    with open(file, 'r') as f:
        data = json.load(f)
        
        # Loop through each tweet in the data
        for tweet in data['data']:
            tweet_id = tweet['id']
            tweet_text = tweet['text']
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

# Close the writer
writer._save()
    
print('Data has been successfully written to bridgerton_tweets.xlsx')