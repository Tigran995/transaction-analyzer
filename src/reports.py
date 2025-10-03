"""Генерация отчетов."""
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

logger = logging.getLogger(__name__)


def report_to_file(filename: Optional[str] = None):
    """Декоратор для сохранения отчета в файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename or f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    if isinstance(result, str):
                        f.write(result)
                    else:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                logger.info(f"Отчет сохранен в {file_name}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета: {e}")

            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(transactions_df: pd.DataFrame, category: str, date_str: Optional[str] = None) -> str:
    """Отчет по тратам в категории за 3 месяца."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
        three_months_ago = target_date - timedelta(days=90)

        # Фильтруем данные
        mask = (transactions_df['Дата операции'] >= three_months_ago) & (
                    transactions_df['Дата операции'] <= target_date)
        period_data = transactions_df[mask]

        # Суммируем траты по категории
        category_spending = period_data[period_data['Категория'] == category]['Сумма платежа'].sum()

        result = {
            "category": category,
            "total_spent": round(category_spending, 2),
            "period_start": three_months_ago.strftime("%Y-%m-%d"),
            "period_end": target_date.strftime("%Y-%m-%d")
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)
