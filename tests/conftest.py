import subprocess
import time
import signal
from pathlib import Path

import grpc
import pytest

import monitor_pb2
import monitor_pb2_grpc


ROOT_DIR = Path(__file__).resolve().parent.parent
BINARY_PATH = ROOT_DIR / "build" / "grpc_udp_monitor"

GRPC_ADDRESS = "127.0.0.1:2031"

STARTUP_TIMEOUT_SEC = 10
POLL_INTERVAL_SEC = 0.2


@pytest.fixture(scope="session")
def app_process():
    process = subprocess.Popen(
        [str(BINARY_PATH)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    channel = grpc.insecure_channel(GRPC_ADDRESS)
    stub = monitor_pb2_grpc.MonitorServiceStub(channel)

    deadline = time.time() + STARTUP_TIMEOUT_SEC
    ready = False

    while time.time() < deadline:
        try:
            response = stub.IsReady(monitor_pb2.Empty())

            if response.is_ready:
                ready = True
                break

        except grpc.RpcError:
            pass

        time.sleep(POLL_INTERVAL_SEC)

    if not ready:
        process.kill()
        raise RuntimeError("Application did not become ready in time")

    yield process

    process.send_signal(signal.SIGINT)

    try:
        return_code = process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        raise RuntimeError("Application did not stop gracefully")

    assert return_code == 0, (
        f"Application exited with non-zero code: {return_code}"
    )