"""Функции для генерации JSON ответов веб-страниц."""
import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: list) -> list:
    """Возвращает курсы валют (заглушка)."""
    mock_rates = {"USD": 95.5, "EUR": 102.3, "GBP": 118.7}
    return [{"currency": curr, "rate": mock_rates.get(curr, 0)} for curr in currencies]


def get_stock_prices(stocks: list) -> list:
    """Возвращает цены акций (заглушка)."""
    mock_prices = {"AAPL": 185.0, "GOOGL": 138.5, "MSFT": 378.2}
    return [{"stock": stock, "price": mock_prices.get(stock, 0)} for stock in stocks]


def main_page(date_str: str, transactions_df: pd.DataFrame, user_settings: Dict[str, Any]) -> str:
    """Генерирует JSON для главной страницы."""
    try:
        # Приветствие
        greeting = get_greeting()

        # Фильтрация данных за месяц
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        start_of_month = target_date.replace(day=1, hour=0, minute=0, second=0)
        mask = (transactions_df['Дата операции'] >= start_of_month) & (transactions_df['Дата операции'] <= target_date)
        monthly_data = transactions_df[mask]

        # Данные по картам
        cards_data = []
        if not monthly_data.empty and 'Номер карты' in monthly_data.columns:
            for card_num, group in monthly_data.groupby('Номер карты'):
                total_spent = group['Сумма платежа'].sum()
                cashback = group['Кешбэк'].sum() if 'Кешбэк' in group.columns else 0
                cards_data.append({
                    "last_digits": str(card_num)[-4:],
                    "total_spent": round(total_spent, 2),
                    "cashback": round(cashback, 2)
                })

        # Топ-5 транзакций
        top_transactions = []
        if not monthly_data.empty:
            top_5 = monthly_data.nlargest(5, 'Сумма платежа')
            for _, row in top_5.iterrows():
                top_transactions.append({
                    "date": row['Дата операции'].strftime("%d.%m.%Y"),
                    "amount": round(row['Сумма платежа'], 2),
                    "category": row.get('Категория', 'Неизвестно'),
                    "description": row.get('Описание', 'Неизвестно')
                })

        # Формируем результат
        result = {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(user_settings.get("user_currencies", [])),
            "stock_prices": get_stock_prices(user_settings.get("user_stocks", []))
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в main_page: {e}")
        return json.dumps({"error": "Внутренняя ошибка сервера"}, ensure_ascii=False)
