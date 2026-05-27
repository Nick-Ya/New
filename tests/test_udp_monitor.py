import subprocess
import time
import socket
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import monitor_pb2
import monitor_pb2_grpc

def test_application_becomes_ready():
    # Запуск приложения в отдельном процессе
    app_process = subprocess.Popen(
        ['./build/grpc_udp_monitor'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)  # Даём время на запуск
    
    # Проверка готовности через gRPC
    channel = grpc.insecure_channel('127.0.0.1:2031')
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)
    
    try:
        response = stub.IsReady(monitor_pb2.Empty())
        assert response.is_ready == True
    finally:
        app_process.terminate()
        app_process.wait()

def test_single_datagram_statistics():
    app_process = subprocess.Popen(
        ['./build/grpc_udp_monitor'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    # Отправка одного датаграмма
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'AAAA', ('127.0.0.1', 2032))
    sock.close()
    
    time.sleep(0.5)
    
    # Получение статистики
    channel = grpc.insecure_channel('127.0.0.1:2031')
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)
    stats = stub.GetUdpStatistics(monitor_pb2.Empty())
    
    assert stats.packets == 1
    assert stats.aBytes == 4
    
    app_process.terminate()
    app_process.wait()

def test_multiple_datagrams_statistics():
    app_process = subprocess.Popen(
        ['./build/grpc_udp_monitor'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Отправка нескольких датаграммов
    sock.sendto(b'AAAA', ('127.0.0.1', 2032))
    time.sleep(0.3)
    sock.sendto(b'BBBB', ('127.0.0.1', 2032))
    time.sleep(0.3)
    sock.sendto(b'AAAA', ('127.0.0.1', 2032))
    
    sock.close()
    time.sleep(0.5)
    
    # Получение статистики
    channel = grpc.insecure_channel('127.0.0.1:2031')
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)
    stats = stub.GetUdpStatistics(monitor_pb2.Empty())
    
    assert stats.packets == 3
    assert stats.aBytes == 8  # 4 + 0 + 4
    
    app_process.terminate()
    app_process.wait()