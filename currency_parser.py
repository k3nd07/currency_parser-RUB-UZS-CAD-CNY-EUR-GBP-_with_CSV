"""Парсер курсов валют (данные Центробанка РФ).

Скачивает актуальные курсы из интернета, показывает таблицу с динамикой
(выросла/упала с прошлого дня), конвертирует суммы между любыми валютами
и сохраняет историю курсов в CSV-файл.
"""

from __future__ import annotations

import csv
import json
import urllib.error
import urllib.request
from pathlib import Path

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
HISTORY_FILE = Path(__file__).with_name("rates_history.csv")
FAVORITES = ["USD", "EUR", "CNY", "GBP", "CAD", "UZS", "TRY", "KZT", "JPY"]
# В каких валютах показывать курсы (колонки таблицы)
SHOW_IN = ["RUB", "UZS", "CAD", "CNY", "EUR", "GBP"]


def fetch_json() -> dict:
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_rates(data: dict) -> dict:
    """Превращает ответ сервера в удобный словарь.

    Результат: {"date": "2026-10-05", "rates": {"USD": {...}, ...}}
    Для каждой валюты считаем цену ОДНОЙ единицы в рублях
    (у некоторых валют номинал 10 или 100, например у йены).
    """
    rates = {"RUB": {"name": "Российский рубль", "price": 1.0, "previous": 1.0}}
    for code, item in data["Valute"].items():
        nominal = item["Nominal"]
        rates[code] = {
            "name": item["Name"],
            "price": item["Value"] / nominal,
            "previous": item["Previous"] / nominal,
        }
    return {"date": data["Date"][:10], "rates": rates}


def convert(amount: float, from_code: str, to_code: str, rates: dict) -> float:
    """Переводим через рубли: сумма -> рубли -> нужная валюта."""
    rubles = amount * rates[from_code]["price"]
    return rubles / rates[to_code]["price"]


def change_text(info: dict) -> str:
    diff = info["price"] - info["previous"]
    percent = diff / info["previous"] * 100 if info["previous"] else 0
    arrow = "▲" if diff > 0 else "▼" if diff < 0 else "="
    return f"{arrow} {percent:+.2f}%"


def fmt(value: float) -> str:
    """Красивое число: большие - с 2 знаками, маленькие - с 4."""
    text = f"{value:,.2f}" if value >= 100 else f"{value:.4f}"
    return text.replace(",", " ")


def print_table(parsed: dict, codes: list) -> None:
    rates = parsed["rates"]
    columns = [c for c in SHOW_IN if c in rates]
    print(f"\nСтоимость 1 единицы валюты на {parsed['date']}")
    header = f"{'Код':<5}{'Валюта':<18}"
    header += "".join(f"{'в ' + c:>12}" for c in columns)
    header += "   К ₽ за день"
    print(header)
    print("-" * len(header))
    for code in codes:
        info = rates.get(code)
        if not info:
            continue
        row = f"{code:<5}{info['name'][:16]:<18}"
        for target in columns:
            row += f"{fmt(convert(1, code, target, rates)):>12}"
        row += f"   {change_text(info)}"
        print(row)


def save_history(parsed: dict) -> bool:
    """Дописывает курсы дня в CSV. Если этот день уже сохранён - пропускает."""
    saved_dates = set()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, newline="", encoding="utf-8-sig") as f:
            saved_dates = {row[0] for row in csv.reader(f, delimiter=";")}
    if parsed["date"] in saved_dates:
        return False
    is_new = not HISTORY_FILE.exists()
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        if is_new:
            writer.writerow(["Дата", "Валюта", "Курс"])
        for code, info in parsed["rates"].items():
            writer.writerow([parsed["date"], code, round(info["price"], 4)])
    return True


def ask_code(prompt: str, rates: dict) -> str:
    while True:
        code = input(prompt).strip().upper()
        if code in rates:
            return code
        print("Нет такой валюты. Список кодов смотрите в пункте 3.")


def converter(parsed: dict) -> None:
    rates = parsed["rates"]
    try:
        amount = float(input("Сумма: ").replace(",", ".").replace(" ", ""))
    except ValueError:
        print("Нужно ввести число.")
        return
    from_code = ask_code("Из какой валюты (например USD): ", rates)
    to_code = ask_code("В какую валюту (например RUB): ", rates)
    result = convert(amount, from_code, to_code, rates)
    print(f"\n{amount:,.2f} {from_code} = {result:,.2f} {to_code}".replace(",", " "))


def main() -> None:
    print("=== Курсы валют ===")
    print("Загружаю данные...")
    try:
        parsed = parse_rates(fetch_json())
    except (urllib.error.URLError, TimeoutError):
        print("Не удалось подключиться к серверу. Проверьте интернет.")
        return
    except (KeyError, ValueError):
        print("Сервер вернул данные в неожиданном формате.")
        return

    print_table(parsed, FAVORITES)
    while True:
        print("\n1. Основные курсы\n2. Конвертер валют\n3. Все валюты\n"
              "4. Сохранить в CSV\n0. Выход")
        choice = input("Выбор: ").strip()
        if choice == "1":
            print_table(parsed, FAVORITES)
        elif choice == "2":
            converter(parsed)
        elif choice == "3":
            print_table(parsed, sorted(parsed["rates"]))
        elif choice == "4":
            if save_history(parsed):
                print(f"Сохранено в {HISTORY_FILE}")
            else:
                print("Курсы за эту дату уже сохранены.")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
