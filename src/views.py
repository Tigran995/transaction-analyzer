from typing import Dict, List
import pandas as pd
from .utils import load_transactions, get_greeting


def home_page(date_time: str) -> Dict:
    """
    Генерирует JSON для главной страницы.

    Args:
        date_time: Дата в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        {
            "greeting": str,
            "cards": List[Dict],
            "top_transactions": List[Dict],
            "currency_rates": List[Dict],
            "stock_prices": List[Dict]
        }
    """
    df = load_transactions("data/operations.xls")
    current_date = pd.to_datetime(date_time.split()[0])

    # Фильтр транзакций за текущий месяц
    monthly_transactions = df[
        (df['Дата операции'].dt.month == current_date.month) &
        (df['Дата операции'].dt.year == current_date.year)
        ]

    # Анализ по картам
    cards = monthly_transactions.groupby('Номер карты').agg({
        'Сумма операции': 'sum',
        'Кешбэк': 'sum'
    }).reset_index()

    cards_list = [{
        "last_digits": str(card)[-4:],
        "total_spent": round(total, 2),
        "cashback": round(cashback, 2)
    } for card, total, cashback in zip(
        cards['Номер карты'],
        cards['Сумма операции'],
        cards['Кешбэк']
    )]

    # Топ-5 транзакций
    top_transactions = monthly_transactions.nlargest(5, 'Сумма операции')
    top_transactions_list = [{
        "date": row['Дата операции'].strftime('%d.%m.%Y'),
        "amount": round(row['Сумма операции'], 2),
        "category": row['Категория'],
        "description": row['Описание']
    } for _, row in top_transactions.iterrows()]

    return {
        "greeting": get_greeting(),
        "cards": cards_list,
        "top_transactions": top_transactions_list,
        "currency_rates": [{"currency": "USD", "rate": 75.5}],  # Заглушка
        "stock_prices": [{"stock": "AAPL", "price": 150.0}]  # Заглушка
    }
