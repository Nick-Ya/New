import json
import socket
import sys
from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


HOST = "127.0.0.1"
PORT = 2001


class SignalClient:
    """Небольшой TCP-клиент для desktop-приложения."""

    def __init__(self):
        self.sock = None
        self.buffer = b""

    def connect(self):
        self.sock = socket.create_connection((HOST, PORT), timeout=2)
        self.sock.setblocking(False)

    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def receive(self):
        """Читает все доступные TCP-данные и возвращает готовые JSON-сообщения."""
        if not self.sock:
            return []

        try:
            while True:
                chunk = self.sock.recv(65536)
                if not chunk:
                    self.disconnect()
                    return []
                self.buffer += chunk
        except BlockingIOError:
            pass

        result = []

        while b"\n" in self.buffer:
            raw, self.buffer = self.buffer.split(b"\n", 1)
            if raw.strip():
                result.append(json.loads(raw.decode("utf-8")))

        return result


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signal Monitor")
        self.resize(760, 500)

        self.client = SignalClient()

        self.status = QLabel("Статус: отключено")
        self.status.setObjectName("connectionStatus")

        self.connect_button = QPushButton("Подключиться")
        self.connect_button.setObjectName("connectButton")
        self.connect_button.clicked.connect(self.connect_to_server)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.clicked.connect(self.refresh_signals)

        self.table = QTableWidget(0, 5)
        self.table.setObjectName("signalsTable")
        self.table.setHorizontalHeaderLabels(
            ["ID", "Имя", "Значение", "Качество", "Время"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)

        buttons = QHBoxLayout()
        buttons.addWidget(self.connect_button)
        buttons.addWidget(self.refresh_button)
        buttons.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Таймер позволяет автоматически получать изменяющиеся значения.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_signals)
        self.timer.start(500)

    def connect_to_server(self):
        try:
            self.client.connect()
            self.status.setText(f"Статус: подключено к {HOST}:{PORT}")
            self.connect_button.setEnabled(False)
            self.refresh_signals()
        except OSError as exc:
            self.status.setText(f"Ошибка подключения: {exc}")

    def refresh_signals(self):
        try:
            signals = self.client.receive()
        except (OSError, json.JSONDecodeError) as exc:
            self.status.setText(f"Ошибка получения данных: {exc}")
            return

        if not signals:
            return

        # Сервер присылает полный набор из 10 сигналов.
        # Последнее значение каждого ID сохраняем в таблице.
        by_id = {}
        for signal in signals:
            by_id[signal["id"]] = signal

        ordered = [by_id[key] for key in sorted(by_id)]

        self.table.setRowCount(len(ordered))

        for row, signal in enumerate(ordered):
            self.table.setItem(row, 0, QTableWidgetItem(str(signal["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(signal["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(signal["value"])))
            self.table.setItem(row, 3, QTableWidgetItem(signal["quality"]))
            self.table.setItem(row, 4, QTableWidgetItem(signal["time"]))

    def closeEvent(self, event):
        self.client.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
