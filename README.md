# Azure Sentiment Analysis & News API Integration

## Overview
This project is a Python-based ETL (Extract, Transform, Load) tool that integrates multiple REST APIs to perform real-time analysis on global news trends. It demonstrates backend development skills including **API authentication**, **JSON data parsing**, and **Cloud AI integration**.

## Features
* **REST API Integration:** Fetches live news data using the `NewsAPI` service.
* **Cloud AI Services:** Sends text payloads to **Azure Cognitive Services** (Text Analytics API) to determine sentiment (Positive, Negative, Neutral).
* **Batch Processing:** Implements custom chunking logic (`chunk_data`) to handle API rate limits and payload size restrictions.
* **Security:** Uses a custom `key_loader.py` module to handle sensitive API keys securely, preventing credential leakage in version control.

## Technical Details
* **Language:** Python 3.x
* **Data Processing:** Pandas, JSON
* **Networking:** Requests library (HTTP POST/GET)
* **Authentication:** Custom header injection for Azure & API Key parameters for NewsAPI.

## Project Structure
* `news_sentiment_etl.py`: The main logic script that orchestrates the data fetch, analysis, and export.
* `key_loader.py`: A security utility that loads API keys from local files (excluded from git) or handles missing keys gracefully.
* `requirements.txt`: List of dependencies.

## How to Run
**Note:** This repository excludes the actual API keys for security reasons.
To run this locally, you must provide your own keys in the root directory:
1. `news.txt`: Your NewsAPI Key.
2. `azure.txt`: Your Azure Cognitive Services Key.
3. `azure_e.txt`: Your Azure Endpoint URL.

## Example Output
The script generates an Excel report categorizing headlines by sentiment:
| Title | Source | Sentiment |
|-------|--------|-----------|
| AI Regulation laws passed in EU... | BBC News | neutral |
| Tech market surges after new announcement... | Reuters | positive |
| Concerns grow over data privacy... | CNN | negative |
