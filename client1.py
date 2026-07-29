# 실습 1 - 평문(암호화하지 않은) 메시지를 보내는 클라이언트
#
# 이 프로그램을 실행하는 컴퓨터가 "보내는 사람" 역할을 합니다.
# 짝의 컴퓨터에서 실습1_평문_서버.py 를 먼저 실행해두고,
# 그 컴퓨터의 IP 주소를 아래 SERVER_IP 에 입력한 뒤 실행하세요.
#
# IP 주소 확인 방법: 명령 프롬프트(cmd)에서 ipconfig 입력 → IPv4 주소 확인

import socket

SERVER_IP = input("Server ip :")   # 예: "192.168.0.15"
PORT = 5001  # 서버와 반드시 같은 포트 번호를 사용해야 합니다


def send_message(sock, payload: bytes):
    """메시지 앞에 '길이(4바이트)'를 붙여서 보냅니다.
    받는 쪽에서 메시지를 하나씩 정확히 구분할 수 있게 하기 위해서입니다."""
    header = len(payload).to_bytes(4, byteorder="big")
    sock.sendall(header + payload)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print(f"[연결 완료] {SERVER_IP}:{PORT} 서버에 연결되었습니다.")
    print("메시지를 입력해서 보내보세요. 'exit'를 입력하면 프로그램이 끝납니다.\n")

    with client_socket:
        while True:
            message = input("보낼 메시지 > ")
            send_message(client_socket, message.encode("utf-8"))

            if message == "exit":
                print("[프로그램 종료] 'exit' 메시지를 보내고 연결을 마칩니다.")
                break


if __name__ == "__main__":
    main()
