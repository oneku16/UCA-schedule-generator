FROM python:3.12-slim

# Добавляем uv пакетный менеджер
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Установим системные зависимости (например, для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установим переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей отдельно — для layer caching
COPY requirements.txt pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv pip install --system -r requirements.txt

# Копируем весь остальной проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
