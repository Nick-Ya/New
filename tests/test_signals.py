import time
import sys
import subprocess
import pytest
from pywinauto import Desktop

ROOT = r"C:\Users\user\PycharmProjects\signal-monitor-project"
APP = r"application\main.py"


@pytest.fixture
def simulator():
    """Запускаем TCP-симулятор."""
    process = subprocess.Popen(
        [sys.executable, "simulator/server.py"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    yield process
    process.terminate()


@pytest.fixture
def app(simulator):
    """Запускаем desktop-приложение."""
    process = subprocess.Popen(
        [sys.executable, APP],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    window = Desktop(backend="uia").window(title="Signal Monitor")
    window.wait("visible", timeout=10)

    yield window
    process.terminate()


def test_connect_and_receive_10_signals(app):
    """
    Критичный сценарий из тестового задания:
    подключение к сервису и получение всех 10 сигналов.
    """

    # 1. Нажимаем «Подключиться».
    app.child_window(
        auto_id="QApplication.MainWindow.QWidget.connectButton",
        control_type="Button"
    ).click_input()

    # 2. Ждём, пока приложение получит данные.
    table = app.child_window(
        auto_id="QApplication.MainWindow.QWidget.signalsTable",
        control_type="Table"
    )

    deadline = time.time() + 10
    data_rows = []

    while time.time() < deadline:
        # Получаем ВСЕ элементы таблицы
        all_items = table.wrapper_object().items()

        # Фильтруем только строки с данными (исключаем заголовки и пустые панели)
        data_rows = [
            item for item in all_items
            if item.element_info.control_type != "Header"
            and item.element_info.control_type != "Pane"  # <-- ИСКЛЮЧАЕМ Pane
            and item.window_text().strip()  # <-- ИСКЛЮЧАЕМ ПУСТЫЕ СТРОКИ
        ]

        # Проверяем, что есть хотя бы 10 сигналов
        if len(data_rows) >= 10:
            break

        time.sleep(0.5)

    # Главная проверка: должны отображаться минимум 10 сигналов
    assert len(data_rows) >= 10, (
        f"Ожидалось минимум 10 сигналов, но в таблице {len(data_rows)}"
    )

    # Дополнительная проверка: все поля не пустые (уже проверено в фильтре)
    for row in data_rows[:10]:
        row_text = row.window_text()
        assert row_text.strip(), f"Найдена пустая строка в таблице: {row}"