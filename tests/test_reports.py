import pandas as pd
from src.services import profitable_cashback_categories

def test_cashback_categories():
    """Проверяет расчет кешбэка по категориям."""
    test_data = pd.DataFrame([
        {"Дата операции": "2023-01-01", "Категория": "Еда", "Кешбэк": 10},
        {"Дата операции": "2023-01-02", "Категория": "Транспорт", "Кешбэк": 5}
    ])
    result = profitable_cashback_categories(test_data, 2023, 1)
    assert "Еда" in result
    assert result["Еда"] == 10
