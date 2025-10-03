"""Главный модуль приложения."""
import json
import logging
from src.data_loader import load_transactions
from src.views import main_page
from src.services import profitable_cashback_categories, simple_search
from src.reports import spending_by_category

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Основная функция приложения."""
    try:
        # Загрузка настроек
        with open('config/user_settings.json', 'r', encoding='utf-8') as f:
            user_settings = json.load(f)

        # Загрузка данных
        transactions_df = load_transactions('data/operations.xls')
        if transactions_df is None:
            logger.error("Не удалось загрузить данные")
            return

        # Пример использования функций
        print("=== ГЛАВНАЯ СТРАНИЦА ===")
        main_result = main_page("2023-10-15 14:30:00", transactions_df, user_settings)
        print(main_result)

        print("\n=== ВЫГОДНЫЕ КАТЕГОРИИ КЕШБЭКА ===")
        transactions_list = transactions_df.to_dict('records')
        cashback_result = profitable_cashback_categories(transactions_list, 2023, 10)
        print(cashback_result)

        print("\n=== ТРАТЫ ПО КАТЕГОРИИ ===")
        spending_result = spending_by_category(transactions_df, "Супермаркеты", "2023-10-15")
        print(spending_result)

        print("\n=== ПРОСТОЙ ПОИСК ===")
        search_result = simple_search("Такси", transactions_list)
        print(search_result)

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")


if __name__ == "__main__":
    main()