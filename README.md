# Incident API Service

**Задача**
Сделать маленький API-сервис для учёта инцидентов.
**Контекст**: операторы и системы присылают сообщения о проблемах в TG (самокат не в сети, точка не отвечает, отчёт не выгрузился). Не хотим **терять это в чатах.**
---
### Требования
Технологии:
- Python
- Любой знакомый тебе веб-фреймворк (предпочитаем что-то из стека в вакансии: FastAPI/Flask/Django)
- Любое простое персистентное хранилище (SQLite/Postgres/MySQL и тп)
Функциональность:

Инцидент должен иметь:
- id
- текст/описание
- статус (любой вменяемый набор, не 0/1)
- источник (например, operator / monitoring / partner)
- время создания

Нужны 3 вещи:
1. **Создать инцидент**
2. **Получить список инцидентов (с фильтром по статусу)**
3. **Обновить статус инцидента по id**
Если не найден — вернуть 404.

## Стек:
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Pydantic
- Docker

## Как запустить

### 1. Docker

1.  Убедитесь, что у вас установлен Docker и Docker Compose.
2.  Склонируйте репозиторий:
    ```bash
    git clone <URL вашего репозитория>
    cd incident-api-service
    ```
3.  Запустите сервисы:
    ```bash
    docker-compose up --build
    ```
    API будет доступно по адресу `http://localhost:8000`.
    Интерактивная документация (Swagger UI) будет доступна по адресу `http://localhost:8000/docs`.

### 2. Локально (без Docker)

1.  Убедитесь, что у вас установлен Python 3.11 и запущен экземпляр PostgreSQL.
2.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```
3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
4.  Установите переменную окружения для подключения к БД:
    ```bash
    export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/incidentdb"
    ```
    *Замените `user`, `password` и `incidentdb` на ваши данные.*
5.  Запустите приложение:
    ```bash
    uvicorn app.main:app --reload
    ```

## Эндпоинты API

### 1. Создание инцидента

-   **Эндпоинт:** `POST /incidents/`
-   **Описание:** Создает новую запись об инциденте. Статус по умолчанию — `open`.
-   **Тело запроса:** JSON с полями `description` и `source`.

**Пример использования:**
```bash
curl -X 'POST' \
  'http://localhost:8000/incidents/' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Самокат #4567 не отвечает на запросы",
  "source": "monitoring"
}'
```

- **Успешный ответ**
```json
{
  "description": "Самокат #4567 не отвечает на запросы",
  "source": "monitoring",
  "id": 1,
  "status": "open",
  "created_at": "2025-11-08T10:00:00.123Z"
}
```

### 2. Получение списка инцидентов

-   **Эндпоинт:** `GET /incidents/`
-   **Описание:** Возвращает список инцидентов. Можно фильтровать по статусу.

**Пример использования (получить все инциденты):**
```bash
curl -X 'GET' 'http://localhost:8000/incidents/'
```

**Пример использования (получить только открытые инциденты):**
```bash
curl -X 'GET' 'http://localhost:8000/incidents/?status=open'
```

- **Успешный ответ**
```json
[
  {
    "description": "Самокат #4567 не отвечает на запросы",
    "source": "monitoring",
    "id": 1,
    "status": "open",
    "created_at": "2025-11-08T10:00:00.123Z"
  }
]
```


### 3. Обновление инцидента

-   **Эндпоинт:** `PATCH /incidents/{incident_id}`
-   **Описание:** Обновляет статус конкретного инцидента по его id.
-   **Тело запроса:** JSON с полем `status`.
```bash
curl -X 'PATCH' \
  'http://localhost:8000/incidents/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "in_progress"
}'
```

- **Успешный ответ**
```JSON
{
  "description": "Самокат #4567 не отвечает на запросы",
  "source": "monitoring",
  "id": 1,
  "status": "in_progress",
  "created_at": "2025-11-08T10:00:00.123Z"
}
```