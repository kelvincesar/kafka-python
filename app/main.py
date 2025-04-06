import socket  # noqa: F401
import struct

def main() -> None:
    print("Logs from your program will appear here!")

    MESSAGE_SIZE = 1
    CORRELATION_ID = 7
    response = struct.pack(">II", MESSAGE_SIZE, CORRELATION_ID)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 9092))
        s.listen()
        print("Listening on port 9092...")
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while msg := conn.recv(1024):
                    print(f"Received {msg} and sending {response}")
                    conn.sendall(response)
            conn.close()

if __name__ == "__main__":
    main()
