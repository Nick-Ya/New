# UDP Monitor Service (C++ + gRPC + Boost.Asio)

## Описание

Сервис на C++ принимает UDP-датаграммы на `127.0.0.1:2032` и ведёт статистику:

- количество полученных UDP-датаграмм
- количество символов `'A'` во всех полученных сообщениях

Статистика доступна через gRPC API на `127.0.0.1:2031`.

---

## Архитектура

- UDP приёмник реализован на `Boost.Asio`
- gRPC сервер предоставляет API:
  - `IsReady` — готовность сервиса
  - `GetUdpStatistics` — статистика пакетов и символов

---

## Структура проекта


test-task/
├── cpp-application/ # C++ сервер
├── tests/ # pytest тесты
├── build.sh # сборка
├── test.sh # запуск тестов
├── requirements.txt # Python зависимости
└── README.md


---

## Сборка

```bash
chmod +x build.sh test.sh
./build.sh
Запуск приложения
./build/grpc_udp_monitor
Запуск тестов
./test.sh
Ручная проверка UDP
python3 -c "
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'AAAA', ('127.0.0.1', 2032))
sock.close()
"
gRPC API
IsReady

Проверка готовности сервиса

GetUdpStatistics

Возвращает:

packets — количество UDP-датаграмм
aBytes — количество символов 'A'
Зависимости
C++
Boost.Asio
gRPC
Protobuf
Python
pytest
grpcio
grpcio-tools
protobuf