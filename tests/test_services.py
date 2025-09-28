"""Тесты для services.py."""
import pytest
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services import profitable_cashback_categories, simple_search

@pytest.fixture
def sample_transactions():
    """Тестовые транзакции."""
    return [
        {
            'Дата операции': '2023-10-01',
            'Категория': 'Еда',
            'Кешбэк': 10.0,
            'Описание': 'Магазин'
        },
        {
            'Дата операции': '2023-10-02',
            'Категория': 'Транспорт', 
            'Кешбэк': 5.0,
            'Описание': 'Такси'
        }
    ]

def test_profitable_cashback_returns_json(sample_transactions):
    """Тест возврата JSON."""
    result = profitable_cashback_categories(sample_transactions, 2023, 10)
    data = json.loads(result)
    assert isinstance(data, dict)

def test_simple_search_returns_json(sample_transactions):
    """Тест простого поиска."""
    result = simple_search("Магазин", sample_transactions)
    data = json.loads(result)
    assert isinstance(data, list)
