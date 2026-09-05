import json
import math
import socket
import time

HOST = "0.0.0.0"
PORT = 2001
SIGNAL_COUNT = 10


def build_signal(signal_id: int, tick: int) -> dict:
    return {
        "id": signal_id,
        "name": f"Signal_{signal_id}",
        "value": round(math.sin(tick / 5 + signal_id / 3), 3),
        "quality": "GOOD",
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Signal simulator listening on {HOST}:{PORT}")

        while True:
            conn, address = server.accept()
            print(f"Client connected: {address}")

            with conn:
                tick = 0
                while True:
                    messages = []
                    for signal_id in range(1, SIGNAL_COUNT + 1):
                        messages.append(build_signal(signal_id, tick))

                    payload = "\n".join(
                        json.dumps(signal, ensure_ascii=False)
                        for signal in messages
                    ) + "\n"

                    try:
                        conn.sendall(payload.encode("utf-8"))
                    except (BrokenPipeError, ConnectionResetError):
                        print("Client disconnected")
                        break

                    tick += 1
                    time.sleep(1)


if __name__ == "__main__":
    main()
