import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict


def spending_by_category(
        df: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict:
    """
    Анализирует траты по категории за последние 3 месяца.

    Args:
        df: DataFrame с транзакциями.
        category: Название категории (например, "Супермаркеты").
        date: Дата в формате 'YYYY-MM-DD' (опционально).

    Returns:
        {"total": сумма, "transactions": список транзакций}
    """
    end_date = datetime.now() if not date else datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)

    filtered = df[
        (df['Категория'] == category) &
        (df['Дата операции'] >= start_date) &
        (df['Дата операции'] <= end_date)
        ]

    return {
        "total": round(filtered['Сумма операции'].sum(), 2),
        "transactions": filtered.to_dict("records")
    }
