Markdown


# 💱 Real-Time Currency Parser & Matrix Converter

A powerful, zero-dependency Python application that fetches live exchange rate data from the Central Bank of Russia API, normalizes nominal values, displays cross-currency rate matrices, tracks daily market trends, provides an instant multi-currency converter, and logs daily rate history into CSV format.

---

## 🔥 Key Features

* **🌐 Live Financial Data Fetching:** Fetches up-to-date currency exchange data direct from the CBR API with `urllib` and automatic user-agent spoofing to ensure continuous connectivity.
* **📐 Per-Unit Price Normalization:** Automatically adjusts for currency nominal values (e.g., Japanese Yen 100 JPY / Uzbek Som 10,000 UZS) to compute exact individual unit exchange values across all currencies.
* **📊 Dynamic Cross-Currency Matrix:** Generates a real-time table displaying exchange values across multiple reference currencies simultaneously (`RUB`, `UZS`, `CAD`, `CNY`, `EUR`, `GBP`).
* **📈 Daily Trend & Delta Tracking:** Calculates exact percentage variations compared to the previous trading day, featuring clean visual indicators (`▲ +0.45%`, `▼ -0.12%`).
* **🔄 Universal Currency Converter:** Effortlessly converts any amount from currency A to currency B through normalized base calculations.
* **📁 Historical CSV Logger:** Appends daily exchange rates to `rates_history.csv` with built-in duplicate date detection to avoid repeated log entries.
* **⚡ Pure Python Standard Library:** Uses **0 external dependencies** (`urllib`, `json`, `csv`, `pathlib`). Run instantly anywhere Python is installed!

---

## 🛠️ How It Works (Under the Hood)

1. **Data Normalization:** Converts raw API feeds into standardized unit values:
   $$\text{Price per Unit} = \frac{\text{CBR Value}}{\text{Nominal}}$$
2. **Cross-Rate Matrix Calculation:** Converts any pair $(A, B)$ using RUB as the base mediator:
   $$\text{Amount}_B = \text{Amount}_A \times \frac{\text{Price}_A}{\text{Price}_B}$$
3. **Smart Formatting:** Displays large numbers with 2 decimal places and smaller values with up to 4 precision decimals for maximum readability.

---

## 🚀 Quick Start

### Prerequisites
* Python **3.8+** installed on your system.

### Running the Application

Simply clone the repository and execute the script:

```bash
python currency_parser.py
🖥️ Interactive CLI Interface
Plaintext


=== Курсы валют ===
Загружаю данные...

Стоимость 1 единицы валюты на 2026-10-06
Код  Валюта                 в RUB       в UZS       в CAD       в CNY       в EUR       в GBP   К ₽ за день
-----------------------------------------------------------------------------------------------------------
USD  Доллар США             93.45    12,450.20        1.36        7.12        0.91        0.78   ▲ +0.32%
EUR  Евро                  102.10    13,605.00        1.49        7.78        1.00        0.85   ▼ -0.15%
CNY  Китайский юань         13.12     1,748.50        0.19        1.00        0.13        0.11   ▲ +0.08%
UZS  Узбекский сум          0.0075      1.0000      0.0001      0.0006      0.0001      0.0001   = +0.00%

1. Основные курсы
2. Конвертер валют
3. Все валюты
4. Сохранить в CSV
0. Выход
Выбор: 2

Сумма: 100
Из какой валюты (например USD): USD
В какую валюту (например RUB): UZS

100.00 USD = 1 245 020.00 UZS

📄 License
This project is licensed under the MIT License — feel free to modify, distribute, and integrate into your own projects!
