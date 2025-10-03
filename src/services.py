"""Сервисы для анализа транзакций."""
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def profitable_cashback_categories(transactions: List[Dict], year: int, month: int) -> str:
    """Анализирует выгодные категории для кешбэка."""
    try:
        df = pd.DataFrame(transactions)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'])

        # Фильтруем по году и месяцу
        filtered = df[(df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)]

        if filtered.empty:
            return json.dumps({}, ensure_ascii=False)

        # Группируем по категориям
        cashback_by_category = filtered.groupby('Категория')['Кешбэк'].sum().round(2)
        result = cashback_by_category.sort_values(ascending=False).to_dict()

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в profitable_cashback_categories: {e}")
        return json.dumps({}, ensure_ascii=False)


def simple_search(query: str, transactions: List[Dict]) -> str:
    """Простой поиск транзакций."""
    try:
        results = [
            t for t in transactions
            if query.lower() in str(t.get('Описание', '')).lower()
               or query.lower() in str(t.get('Категория', '')).lower()
        ]
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}")
        return json.dumps([], ensure_ascii=False)
