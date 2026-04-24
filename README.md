# Python CSV Processor

CLI-утилита для обработки CSV-файлов на Python.

Проект позволяет читать CSV-файл из командной строки, автоматически приводить числовые значения к нужным типам, фильтровать строки, сортировать данные и выполнять простые агрегирующие операции по числовым столбцам.

## О проекте

`Python CSV Processor` — это небольшая консольная утилита для работы с табличными данными в формате CSV.

Скрипт принимает путь к CSV-файлу и дополнительные аргументы командной строки. С их помощью можно:

- отфильтровать строки по условию;
- отсортировать данные по выбранному столбцу;
- вычислить агрегированное значение по числовому столбцу;
- вывести результат в консоль в виде таблицы.

## Функциональность

### Чтение CSV

- Чтение CSV-файла через стандартный модуль `csv`.
- Автоматическое определение числовых типов данных.
- Преобразование целочисленных значений в `int`.
- Преобразование вещественных значений в `float`.
- Сохранение строковых значений как `str`.

### Фильтрация

Поддерживаются условия:

- `column=value`
- `column>value`
- `column<value`

Примеры:

```bash
--where "brand=xiaomi"
--where "price<500"
--where "rating>4.5"
```

### Сортировка

Поддерживается сортировка по выбранному столбцу:

- `asc` — по возрастанию;
- `desc` — по убыванию.

Примеры:

```bash
--order-by "price=asc"
--order-by "rating=desc"
```

### Агрегация

Поддерживаются агрегирующие операции по числовым столбцам:

- `max` — максимальное значение;
- `min` — минимальное значение;
- `avg` — среднее значение.

Примеры:

```bash
--aggregate "price=max"
--aggregate "rating=avg"
```

## Tech Stack

**Language:** Python

**CLI:** argparse

**CSV processing:** csv

**Output formatting:** tabulate

**Testing:** pytest

## Структура проекта

```text
.
├── main.py          # Основная логика CLI-утилиты
├── _test.py         # Тесты для функций обработки данных
├── example.csv      # Пример входного CSV-файла
├── example_1.png    # Пример работы скрипта
├── example_2.png    # Пример работы скрипта
├── requirements.txt # Зависимости проекта
└── README.md
```

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/KororokisRock/PythonCSVScript.git
cd PythonCSVScript
```

### 2. Создать виртуальное окружение

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

## Использование

Базовый формат запуска:

```bash
python main.py --file example.csv
```

Дополнительные аргументы:

| Argument | Description | Example |
|---|---|---|
| `--file` | Путь к CSV-файлу | `--file example.csv` |
| `--where` | Условие фильтрации | `--where "price<500"` |
| `--order-by` | Сортировка по столбцу | `--order-by "rating=desc"` |
| `--aggregate` | Агрегация по числовому столбцу | `--aggregate "price=max"` |

## Пример CSV-файла

Пример входного файла `example.csv`:

```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
```

## Примеры команд

### Вывести CSV-файл в виде таблицы

```bash
python main.py --file example.csv
```

### Отфильтровать товары дешевле 500

```bash
python main.py --file example.csv --where "price<500"
```

### Отфильтровать товары бренда Xiaomi

```bash
python main.py --file example.csv --where "brand=xiaomi"
```

### Отсортировать товары по рейтингу по убыванию

```bash
python main.py --file example.csv --order-by "rating=desc"
```

### Найти максимальную цену

```bash
python main.py --file example.csv --aggregate "price=max"
```

### Найти средний рейтинг

```bash
python main.py --file example.csv --aggregate "rating=avg"
```

### Совместить фильтрацию и сортировку

```bash
python main.py --file example.csv --where "price<1000" --order-by "rating=desc"
```

### Совместить фильтрацию и агрегацию

```bash
python main.py --file example.csv --where "brand=xiaomi" --aggregate "price=max"
```

## Примеры вывода

![Пример работы](example_1.png)

![Пример работы](example_2.png)

## Тестирование

Для запуска тестов:

```bash
pytest _test.py
```

Или просто:

```bash
pytest
```

Тесты проверяют:

- определение целочисленных значений;
- определение вещественных значений;
- чтение CSV-файла;
- автоматическое преобразование типов;
- фильтрацию строк;
- сортировку данных;
- агрегирующие операции `max`, `min`, `avg`.

## Ограничения

- Фильтрация поддерживает только одно условие за один запуск.
- Условия должны передаваться в формате `column=value`, `column>value` или `column<value`.
- Сортировка должна передаваться в формате `column=asc` или `column=desc`.
- Агрегация должна передаваться в формате `column=max`, `column=min` или `column=avg`.
- Агрегация работает только с числовыми столбцами.
- Среднее значение округляется до двух знаков после запятой.
