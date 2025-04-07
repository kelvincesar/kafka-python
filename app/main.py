import socket  # noqa: F401
from concurrent.futures import ThreadPoolExecutor
import signal
import sys
from app.kafka_types import RequestMessage, ResponseMessage, HEADER_SIZE


def handle_sigint(sig, frame):
    print("\nShutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def parse_message_size(header: bytes) -> int:
    return int.from_bytes(header, byteorder='big', signed=False)

def handle_connection(conn: socket.socket, addr: str) -> None:
    with conn:
        print("Connected by", addr)
        while header := conn.recv(4):
            # check for the message size
            msg_len = parse_message_size(header)
            print(f"Message length: {msg_len}")

            # wait for the rest of the message
            payload = conn.recv(msg_len + HEADER_SIZE)
            request = RequestMessage.from_bytes(payload)
            print(f"Received request: {request}")

            # build the response
            response = ResponseMessage.from_request(request)
            conn.sendall(response.to_bytes())
        conn.shutdown(socket.SHUT_WR)
        conn.close()

def main() -> None:
    print("Logs from your program will appear here!")


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 9092))
        s.listen()
        print("Listening on port 9092...")
        while True:
            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    conn, addr = s.accept()
                    executor.submit(handle_connection, conn, addr)
            

if __name__ == "__main__":
    main()
