# Bridgerton Tweets Analysis

This Python script is designed to extract tweets related to the Bridgerton series. It fetches tweets using the Twitter API, processes them, and saves the results in an Excel file for further analysis.

The Tweets were extracted between the dates of 2024-06-12 and 2024-06-14. The resulting dataset can be seen in the `bridgerton_tweets.xlsx` file.

The following query was used to fetch the tweets:
```
Bridgerton (Michael OR Francesca OR Michaela OR Frannie) until:2024-06-15 since:2024-06-12
```

The final API query was:
```
https://api.twitter.com/2/tweets/search/recent?start_time=2024-06-12T23:59:59Z&end_time=2024-06-15T23:59:59Z&max_results=100&next_token=&tweet.fields=lang,text,public_metrics&query=Bridgerton (Michael OR Francesca OR Michaela OR Frannie)
```
> [!NOTE]
> We have limited the number of API calls to 100 for the research sample.

> [!NOTE]
> We have attempted to use sentiment analysis libraries to analyze the tweets. However, the results were not satisfactory. Therefore, we have decided to remove the sentiment analysis part from the results, but the code is still available in the script.

## Features

- **Data Collection**: Fetches recent tweets based on a specific search query.
- **Data Processing**: Extracts relevant information from tweets.
- **Data Storage**: Saves the processed data into an Excel file for easy analysis.

## Prerequisites

Before running this script, ensure you have the following:

- Python 3.x installed on your system.
- A Twitter Developer account (with at least a `Pro` subscription) and a Bearer Token for API access.
- The following Python libraries installed.
    - requests
    - pandas
    - openpyxl
    - torch *
    - transformers *
    - torchvision *
    - tensorfow *

> [!IMPORTANT]
> Libraries market with `*` are required for the sentiment analysis part of the script. If do not with to use this feature, you can remove the code related to it.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/pedrolacerda/bridgerton-tweets-extraction.git
```

1. Navigate to the cloned repository directory:
```bash
cd bridgerton-tweets-analysis
```

1. Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Configuration

You need to set up your Twitter API Bearer Token in the `config.py` file. See the `config-example.py` file for reference.

## Usage

To start the Tweet extraction, run the script with the following command:
```bash
python main.py
```
