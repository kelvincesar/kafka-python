import socket  # noqa: F401
import struct
import signal
import sys
from app.kafka_types import RequestMessage, ResponseMessage


def handle_sigint(sig, frame):
    print("\nShutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)


def main() -> None:
    print("Logs from your program will appear here!")


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 9092))
        s.listen()
        print("Listening on port 9092...")
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while msg := conn.recv(1024):
                    request = RequestMessage.from_bytes(msg)
                    print(f"Received request: {request}")
                    response = ResponseMessage.from_request(request)
                    conn.sendall(response.to_bytes())
                conn.shutdown(socket.SHUT_WR)
                conn.close()

if __name__ == "__main__":
    main()
