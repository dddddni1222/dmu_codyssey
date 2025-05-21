import zipfile
import threading
import itertools
import string
import time

# 공유 플래그와 결과 저장용 변수
found_password = None
stop_event = threading.Event()

def try_password(zip_path, password):
    """비밀번호 시도 함수"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(pwd=password.encode())  # 비밀번호로 압축 해제 시도
        return True
    except Exception:
        return False

def generate_passwords_forward(max_length):
    """순방향 비밀번호 생성 (a부터)"""
    chars = string.ascii_lowercase  # a-z
    for length in range(1, max_length + 1):
        for pwd in itertools.product(chars, repeat=length):
            yield ''.join(pwd)

def generate_passwords_backward(max_length):
    """역방향 비밀번호 생성 (z부터)"""
    chars = string.ascii_lowercase[::-1]  # z-a
    for length in range(1, max_length + 1):
        for pwd in itertools.product(chars, repeat=length):
            yield ''.join(pwd)

def crack_password_forward(zip_path, max_length):
    """순방향 스레드: a부터 시작"""
    global found_password
    for password in generate_passwords_forward(max_length):
        if stop_event.is_set():  # 다른 스레드가 비밀번호를 찾았으면 종료
            break
        if try_password(zip_path, password):
            found_password = password
            stop_event.set()  # 비밀번호 찾았음을 알림
            print(f"비밀번호 발견 (순방향): {password}")
            break

def crack_password_backward(zip_path, max_length):
    """역방향 스레드: z부터 시작"""
    global found_password
    for password in generate_passwords_backward(max_length):
        if stop_event.is_set():  # 다른 스레드가 비밀번호를 찾았으면 종료
            break
        if try_password(zip_path, password):
            found_password = password
            stop_event.set()  # 비밀번호 찾았음을 알림
            print(f"비밀번호 발견 (역방향): {password}")
            break

def main():
    zip_path = "example.zip"  # 대상 ZIP 파일
    max_length = 3  # 비밀번호 최대 길이 (필요에 따라 수정)

    # 스레드 생성
    thread_forward = threading.Thread(target=crack_password_forward, args=(zip_path, max_length))
    thread_backward = threading.Thread(target=crack_password_backward, args=(zip_path, max_length))

    # 스레드 시작
    start_time = time.time()
    thread_forward.start()
    thread_backward.start()

    # 스레드 종료 대기
    thread_forward.join()
    thread_backward.join()

    # 결과 출력
    if found_password:
        print(f"최종 비밀번호: {found_password}")
        print(f"소요 시간: {time.time() - start_time:.2f}초")
    else:
        print("비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    main()