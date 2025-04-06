import socket  # noqa: F401
import struct
import signal
import sys

def handle_sigint(sig, frame):
    print("\nShutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def parse_message_header(data: bytes) -> tuple:
    # > Big endian
    # I Unsigned int (4 bytes)
    message_size, _, correlation_id = struct.unpack(">III", data[:12])
    return message_size, correlation_id

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
                    message_size, correlation_id = parse_message_header(msg)
                    response = struct.pack(">II", message_size, correlation_id)
                    print(f"Received {msg}: {message_size=}, {correlation_id=} ({response})")
                    conn.sendall(response)
                conn.shutdown(socket.SHUT_WR)
                conn.close()

if __name__ == "__main__":
    main()
