import pytest
from unittest.mock import patch, MagicMock
from src.views import home_page
from datetime import datetime
import pandas as pd

@pytest.fixture
def mock_transactions():
    return pd.DataFrame({
        'Дата операции': ['2023-01-01', '2023-01-02'],
        'Номер карты': ['123456789012', '123456789012'],
        'Сумма операции': [1000, 500],
        'Кешбэк': [10, 5],
        'Категория': ['Food', 'Transport'],
        'Описание': ['Grocery', 'Taxi']
    })

@pytest.fixture
def mock_apis():
    with patch('src.utils.get_currency_rates') as mock_curr, \
         patch('src.utils.get_stock_prices') as mock_stock:
        mock_curr.return_value = [{"currency": "USD", "rate": 75.5}]
        mock_stock.return_value = [{"stock": "AAPL", "price": 150.0}]
        yield

@pytest.mark.parametrize("test_input,expected", [
    ("2023-01-01 12:00:00", ["Добрый день"]),
    ("2023-01-01 05:00:00", ["Доброе утро"]),
])
def test_home_page(test_input, expected, mock_transactions, mock_apis):
    with patch('src.utils.load_transactions', return_value=mock_transactions):
        result = home_page(test_input)
        assert any(greeting in result["greeting"] for greeting in expected)
        assert len(result["cards"]) == 1
        assert len(result["top_transactions"]) <= 2
