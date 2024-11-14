# Pet-project

# Cryptocurrency Analytics and Visualization API

Этот проект представляет собой API на Flask для получения аналитики по криптовалютам, графиков изменений цены, а также данных о текущей стоимости. Используя сторонний API CryptoCompare, приложение позволяет запрашивать данные по выбранной криптовалюте, выводить аналитику и визуализировать изменения цены.

## Функциональность

- **Получение текущей цены криптовалюты**: Endpoint возвращает актуальную стоимость выбранной криптовалюты в указанной валюте.
- **Исторические данные по цене**: Возможность запрашивать данные за последний час или день, с указанием предела выборки.
- **Аналитика цен**: Получение базовой статистики по историческим данным, включая среднюю, медианную цену, минимальное и максимальное значения.
- **Визуализация**: Графическое представление изменения цены с отображением процентного изменения между точками данных. Увеличения и снижения цены отмечены разными цветами.

## Endpoints

1. **`/<cryptocurrency>/latest/<currency>`**: Получение текущей цены.
   - `cryptocurrency`: Аббревиатура криптовалюты (например, BTC).
   - `currency`: Целевая валюта (например, USD).
   
2. **`/<cryptocurrency>/<time>/<currency>/<limit>`**: Исторические данные по цене.
   - `time`: Период данных (`hour` или `day`).
   - `currency`: Валюта.
   - `limit`: Количество записей.

3. **`/<crypto>/analytics/<currency>/<time>/<limit>`**: Получение аналитики по цене.
   - Возвращает среднюю, медианную, минимальную и максимальную цену за указанный период.

4. **`/<crypto>/plot/<currency>/<time>/<limit>`**: Визуализация изменения цены.
   - Генерирует график с указанием процентного изменения между временными метками.

## Установка и настройка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt

3. Создайте файл .env и добавьте свой API ключ от CryptoCompare:
    ```bash
    API_KEY=your_api_key_here

4. Запустите сервер:
    ```bash
    python app.py

## Примеры запросов
1. Получение текущей цены биткоина в долларах:
    ```bash
    GET http://localhost:5000/BTC/latest/USD

2. Исторические данные за последние 10 часов для эфира в евро:
    ```bash
    GET http://localhost:5000/ETH/hour/EUR/10

3. Получение аналитики по цене биткоина за последние 24 дня в долларах:
    ```bash
    GET http://localhost:5000/BTC/analytics/USD/day/24

4. Визуализация цены эфира за последний час в долларах:
    ```bash
    GET http://localhost:5000/ETH/plot/USD/hour/1

## Технологии

    Flask — фреймворк для создания веб-приложений на Python.
    Matplotlib — библиотека для визуализации данных.
    Pandas — библиотека для анализа и обработки данных.
    CryptoCompare API — внешний API для получения информации по криптовалютам.

## Планы на будущее

    Добавление поддержки валют.
    Расширение типов аналитики и возможностей визуализации.
    Добавление функции кэширования данных для снижения нагрузки на внешний API.