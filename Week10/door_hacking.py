import string

# 간단한 사전 키워드 (필요 시 확장 가능)
DICTIONARY = {"the", "this", "message", "secret", "love", "password", "hello", "world", "test", "emergency", "mars"}

def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 자리수 0~25까지 복호화 시도.
    사전 키워드가 등장하면 즉시 중단하고 결과 출력 및 저장.
    """
    print("[INFO] 카이사르 복호화 시작.")
    for shift in range(26):
        decoded = ''
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char

        print(f"[Shift {shift}] {decoded}")

        # 사전 키워드 탐지
        words = decoded.lower().split()
        for word in words:
            if word.strip(string.punctuation) in DICTIONARY:
                print(f"\n[FOUND] 사전 단어 '{word}' 발견! 시프트 {shift}에서 복호화 성공.")
                with open("result.txt", "w", encoding="utf-8") as f:
                    f.write(decoded)
                return decoded

    print("[FAIL] 사전 키워드가 포함된 문장을 찾을 수 없습니다.")
    return None


def main():
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            encrypted = f.read().strip()
            print(f"[READ] 암호문: {encrypted}")
    except FileNotFoundError:
        print("[ERROR] password.txt 파일이 없습니다.")
        return

    caesar_cipher_decode(encrypted)


if __name__ == "__main__":
    main()
