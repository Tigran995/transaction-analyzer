"""Тесты для views.py."""
import pytest
import json
import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.views import main_page, get_greeting


@pytest.fixture
def sample_transactions():
    """Тестовые данные транзакций."""
    return pd.DataFrame({
        'Дата операции': pd.to_datetime(['2023-10-01', '2023-10-02', '2023-10-03']),
        'Номер карты': ['1234', '1234', '5678'],
        'Сумма платежа': [100.0, 200.0, 300.0],
        'Кешбэк': [1.0, 2.0, 3.0],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Описание': ['Магазин', 'Такси', 'Ресторан']
    })


@pytest.fixture
def user_settings():
    """Тестовые настройки пользователя."""
    return {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}


def test_main_page_returns_valid_json(sample_transactions, user_settings):
    """Тест возврата валидного JSON."""
    result = main_page("2023-10-03 12:00:00", sample_transactions, user_settings)
    data = json.loads(result)

    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
    assert isinstance(data["cards"], list)


def test_main_page_structure(sample_transactions, user_settings):
    """Тест структуры ответа."""
    result = main_page("2023-10-03 12:00:00", sample_transactions, user_settings)
    data = json.loads(result)

    # Проверяем наличие всех обязательных полей
    required_fields = ["greeting", "cards", "top_transactions", "currency_rates", "stock_prices"]
    for field in required_fields:
        assert field in data