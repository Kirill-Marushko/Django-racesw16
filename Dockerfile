FROM python:3.11-slim

# Робоча директорія
WORKDIR /app

# Залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . .

# Змінні середовища
ENV PYTHONUNBUFFERED=1

# Команда для запуску (gunicorn)
CMD ["gunicorn", "Django_races.wsgi:application", "--bind", "0.0.0.0:8000"]