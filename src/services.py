import pandas as pd
from typing import Dict


def profitable_cashback_categories(
        df: pd.DataFrame,
        year: int,
        month: int
) -> Dict[str, float]:
    """
    Возвращает категории с наибольшим кешбэком за указанный месяц.

    Args:
        df: DataFrame с транзакциями.
        year: Год (например, 2023).
        month: Месяц (1-12).

    Returns:
        {"Категория": сумма_кешбэка}
    """
    filtered = df[
        (df['Дата операции'].dt.year == year) &
        (df['Дата операции'].dt.month == month)
        ]
    cashback_by_category = filtered.groupby('Категория')['Кешбэк'].sum()
    return cashback_by_category.sort_values(ascending=False).to_dict()
