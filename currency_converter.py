import requests
import logging

RATES_URL = "https://api.exchangerate-api.com/v4/latest/USD"


class CurrencyConverter:
    _rates = None
    _logger = None

    # Инициализация логгера один раз для всего класса
    @classmethod
    def _init_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger("CurrencyConverter")
            cls._logger.setLevel(logging.INFO)
            if not cls._logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)

    @classmethod
    def _fetch_rates(cls):
        if cls._rates is None:
            cls._init_logger()
            cls._logger.info("Fetching exchange rates from API")
            try:
                response = requests.get(RATES_URL)
                response.raise_for_status()
                data = response.json()
                cls._rates = data.get("rates", {})
                cls._logger.info("Exchange rates fetched successfully")
            except Exception as e:
                cls._logger.error(f"Failed to fetch exchange rates: {e}")
                raise
        return cls._rates

    @classmethod
    def convert(cls, amount: float, target_currency: str) -> float:
        """
        Конвертирует сумму из USD в target_currency.

        :param amount: сумма в USD
        :param target_currency: целевая валюта ("RUB", "EUR", "GBP", "CNY")
        :return: конвертированная сумма
        :raises ValueError: если курс для указанной валюты не найден
        """
        cls._init_logger()
        rates = cls._fetch_rates()
        rate = rates.get(target_currency.upper())
        if rate is None:
            cls._logger.error(f"{target_currency.upper()} rate not found.")
            raise ValueError(f"Курс для валюты {target_currency.upper()} не найден.")
        cls._logger.info(f"Converting USD to {target_currency.upper()} using rate: {rate}")
        return amount * rate
