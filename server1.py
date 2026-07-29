# 실습 1 - 평문(암호화하지 않은) 메시지를 받는 서버
#
# 이 프로그램을 실행하는 컴퓨터가 "받는 사람" 역할을 합니다.
# 같은 네트워크 안의 다른 컴퓨터에서 실습1_평문_클라이언트.py 를 실행해
# 이 서버로 메시지를 보내면, 그 내용이 그대로 화면에 출력됩니다.
#
# [실습 목표] 와이어샤크로 이 통신을 캡처했을 때, 메시지 내용이
# 패킷 안에 '있는 그대로' 보인다는 것을 확인합니다.

import socket

HOST = "0.0.0.0"   # 모든 네트워크 카드에서 연결을 받겠다는 의미
PORT = 5001         # 클라이언트와 반드시 같은 포트 번호를 사용해야 합니다


def recv_exact(sock, n):
    """정확히 n바이트를 받을 때까지 계속 읽어옵니다.
    (한 번의 recv()로 메시지 전체가 오지 않을 수도 있기 때문입니다.)"""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def recv_message(sock):
    """맨 앞 4바이트로 메시지 길이를 먼저 읽은 뒤, 그 길이만큼 본문을 읽습니다.
    이렇게 하면 메시지 두 개가 뒤섞이지 않고 하나씩 정확히 구분됩니다."""
    header = recv_exact(sock, 4)
    if header is None:
        return None
    length = int.from_bytes(header, byteorder="big")
    return recv_exact(sock, length)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[서버 시작] {PORT}번 포트에서 클라이언트의 연결을 기다립니다...")
    print("※ 지금부터 와이어샤크에서 캡처를 시작하세요. (필터: tcp.port == 5001)")

    conn, addr = server_socket.accept()
    print(f"[연결됨] {addr} 에서 접속했습니다.\n")

    with conn:
        while True:
            data = recv_message(conn)
            if data is None:
                print("[연결 종료] 클라이언트와의 연결이 끊어졌습니다.")
                break

            message = data.decode("utf-8")
            print(f"[받은 메시지 - 평문] {message}")

            if message == "exit":
                print("[프로그램 종료] 'exit' 메시지를 받아 서버를 마칩니다.")
                break

    server_socket.close()


if __name__ == "__main__":
    main()
