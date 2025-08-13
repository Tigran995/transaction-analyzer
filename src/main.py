import pandas as pd
from datetime import datetime
import logging
import requests
import json
import os
from typing import Dict, List

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

def load_transactions(file_path: str) -> pd.DataFrame:
    """Load transactions from Excel file."""
    try:
        df = pd.read_excel(file_path)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'])
        return df
    except Exception as e:
        logger.error(f"Error loading file: {e}")
        raise

def get_greeting() -> str:
    """Get time-based greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"

def get_currency_rates(currencies: List[str]) -> List[Dict]:
    """Get currency rates from API."""
    try:
        api_key = os.getenv('CURRENCY_API_KEY')
        response = requests.get(
            f"https://api.example.com/currencies?access_key={api_key}&symbols={','.join(currencies)}"
        )
        response.raise_for_status()
        return json.loads(response.text)['rates']
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        return []

def get_stock_prices(stocks: List[str]) -> List[Dict]:
    """Get stock prices from API."""
    try:
        api_key = os.getenv('STOCK_API_KEY')
        response = requests.get(
            f"https://api.example.com/stocks?symbols={','.join(stocks)}&token={api_key}"
        )
        response.raise_for_status()
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Stock API error: {e}")
        return []
