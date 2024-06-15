## Overview

This repository contains a Python script designed to fetch and analyze tweets related to the TV series "Bridgerton". The script collects tweets from JSON files, extracts relevant information, and compiles it into an Excel spreadsheet for further analysis.

## Features

- **Data Extraction:** Extracts tweet data from JSON files matching the pattern `tweets_*.json`.
- **Data Compilation:** Compiles tweet data into a pandas DataFrame with columns for tweet ID, text, language, retweet count, reply count, like count, quote count, bookmark count, and impression count.
- **Excel Export:** Exports the compiled data into an Excel file named `bridgerton_tweets.xlsx` with a dedicated sheet for tweets.

## Requirements

To run this script, you need the following:

- Python 3.x
- pandas
- openpyxl
- glob

## Installation

1. Ensure Python 3.x is installed on your system.
1. Install the required Python packages using pip:
```bash
pip install pandas openpyxl glob2
```

## Usage

1. Place your JSON files containing tweets in the directory `./tweets`. Ensure they match the pattern `tweets_*.json`.
1. Run the script using Python:
```bash
python tweets_json_to_excel.py
```
3. Once the script completes, check the current directory for the `bridgerton_tweets.xlsx` file.