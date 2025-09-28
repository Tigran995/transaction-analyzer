"""Загрузка данных из Excel файла."""
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def load_transactions(file_path: str) -> Optional[pd.DataFrame]:
    """Загружает транзакции из Excel файла."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Успешно загружено {len(df)} транзакций из {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки файла {file_path}: {e}")
        return None
