#!/usr/bin/env bash
set -euo pipefail

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Запуск тестов с увеличенным таймаутом
pytest -v --timeout=10