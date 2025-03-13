def get_file_path_from_user():
    # 샘플 경로
    sample_path = r'C:\Users\YourUsername\Desktop\mission_computer_main.log'
    
    # 사용자에게 경로 입력 받기
    file_path = input(f'불러 올 파일의 경로를 입력해 주세요. (e.g., {sample_path}): ').strip('"')
   
    return file_path

def read_file(file_path):
    try:
        # 파일을 읽기 모드로 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'파일이 존재하지 않습니다. {file_path}')
        return None

def save_to_markdown(log_data, save_path):
    if log_data is None:
        return

    lines = log_data.strip().split('\n')[1:]

    # 메시지의 최대 길이 계산
    max_message_length = max(len(line.split(',', 2)[2]) for line in lines)

    # 고정된 길이
    fixed_timestamp_length = 19 
    fixed_event_length = 5

    # 마크다운 헤더 및 구분선 생성
    md_content  = f"|{'Timestamp'.ljust(fixed_timestamp_length)}|{'Event'.ljust(fixed_event_length)}|{'Message'.ljust(max_message_length)}|\n"
    md_content += f"|{'-' * fixed_timestamp_length}|{'-' * fixed_event_length}|{'-' * max_message_length}|\n"

    # 각 줄을 파싱하여 마크다운 테이블 형식으로 추가
    for i, line in enumerate(lines):
        timestamp, event, message = line.split(",", 2)
        # 마지막 줄에서는 \n을 추가하지 않음
        if i == len(lines) - 1:
            md_content += f"|{timestamp.ljust(fixed_timestamp_length)}|{event.ljust(fixed_event_length)}|{message.ljust(max_message_length)}|"
        else:
            md_content += f"|{timestamp.ljust(fixed_timestamp_length)}|{event.ljust(fixed_event_length)}|{message.ljust(max_message_length)}|\n"

    # 마크다운 파일로 저장
    try:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(md_content)
        print(f'파일 저장 완료: {save_path}')
    except Exception as e:
        print(f'파일 저장 오류: {e}')

def main():
    file_path = get_file_path_from_user()  
    log_data = read_file(file_path) 
    
    print(f'읽어온 파일 내용 : \n{log_data}')

    save_file_name = 'log_analysis.md'
    
    save_to_markdown(log_data, save_file_name)

if __name__ == '__main__':
    main()
