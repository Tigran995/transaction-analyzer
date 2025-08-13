from datetime import datetime
from typing import Dict, List
import pandas as pd
from .utils import load_transactions, get_greeting, get_currency_rates, get_stock_prices
import logging
import json

logger = logging.getLogger(__name__)


def home_page(date_time: str) -> Dict:
    """Generate home page JSON response."""
    try:
        # Parse input date
        current_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        # Load and filter transactions
        df = load_transactions("data/operations.xls")
        monthly_transactions = df[
            (df['Дата операции'].dt.month == current_date.month) &
            (df['Дата операции'].dt.year == current_date.year)
            ]

        # Process cards data
        cards_data = monthly_transactions.groupby('Номер карты').agg({
            'Сумма операции': 'sum',
            'Кешбэк': 'sum'
        }).reset_index()

        cards = [{
            "last_digits": str(card)[-4:],
            "total_spent": round(total, 2),
            "cashback": round(cashback, 2)
        } for card, total, cashback in zip(
            cards_data['Номер карты'],
            cards_data['Сумма операции'],
            cards_data['Кешбэк']
        )]

        # Get top transactions
        top_transactions = monthly_transactions.nlargest(5, 'Сумма операции')
        top_transactions_list = [{
            "date": row['Дата операции'].strftime('%d.%m.%Y'),
            "amount": round(row['Сумма операции'], 2),
            "category": row['Категория'],
            "description": row['Описание']
        } for _, row in top_transactions.iterrows()]

        # Get external data
        currency_rates = get_currency_rates(["USD", "EUR"])
        stock_prices = get_stock_prices(["AAPL", "GOOGL"])

        return {
            "greeting": get_greeting(),
            "cards": cards,
            "top_transactions": top_transactions_list,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

    except Exception as e:
        logger.error(f"Error in home_page: {e}")
        return json.dumps({"error": str(e)})
