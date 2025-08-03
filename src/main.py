from views import home_page
from services import profitable_cashback_categories
from reports import spending_by_category

if __name__ == "__main__":
    # Пример использования
    print(home_page("2023-01-01 12:00:00"))
    print(profitable_cashback_categories(load_transactions("data/operations.xls"), 2023, 1))
