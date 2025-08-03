import pytest
from src.views import home_page
from datetime import datetime

def test_home_page_structure():
    """Проверяет структуру ответа home_page."""
    result = home_page("2023-01-01 12:00:00")
    assert "greeting" in result
    assert isinstance(result["cards"], list)
    assert len(result["top_transactions"]) <= 5
