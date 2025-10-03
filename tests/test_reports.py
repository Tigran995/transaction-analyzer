"""Тесты для reports.py."""
import pytest
import json
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.reports import spending_by_category


@pytest.fixture
def sample_dataframe():
    """Тестовый DataFrame."""
    return pd.DataFrame({
        'Дата операции': pd.date_range('2023-08-01', periods=10, freq='D'),
        'Категория': ['Еда'] * 5 + ['Транспорт'] * 5,
        'Сумма платежа': [100.0] * 10
    })


def test_spending_by_category_returns_json(sample_dataframe):
    """Тест возврата JSON."""
    result = spending_by_category(sample_dataframe, "Еда", "2023-10-01")
    data = json.loads(result)

    assert "category" in data
    assert "total_spent" in data
    assert data["category"] == "Еда"
