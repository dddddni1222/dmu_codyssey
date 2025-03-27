import random

LOG_FILE = r'\mars_base_log.txt'
current_file_path = __file__  # 현재 실행 중인 파일의 경로
LOG_FILE_PATH = current_file_path.rsplit('\\', 1)[0] + LOG_FILE

class DummySensor:
    def __init__(self):
        # 환경 변수들을 담은 사전 객체 (env_values)
        self.env_values = {
            'mars_base_internal_temperature': (18, 30),
            'mars_base_external_temperature': (0, 21),
            'mars_base_internal_humidity': (50, 60),
            'mars_base_external_illuminance': (500, 715),
            'mars_base_internal_co2': (0.02, 0.1),
            'mars_base_internal_oxygen': (4, 7)
        }
        
    # 환경 변수 값을 설정하는 메서드
    def set_env(self):
        # 사전의 각 항목에 대해 랜덤 값을 설정
        for key, (min_val, max_val) in self.env_values.items():
            self.env_values[key] = random.uniform(min_val, max_val)

    # 환경 변수 값을 출력하는 메서드
    def get_env(self):
        
        # 날짜 입력받기
        user_input = input("날짜를 입력하세요 (형식: YYYY-MM-DDThh:mm) ")

        # 날짜 형식 확인
        try:
            # 입력값을 "-" 기준으로 나누어 년, 월, 일로 분리
            date, time = user_input.split('T')
            year, month, day = date.split('-')
            hour, minu = time.split(':')

            # 연도, 월, 일이 숫자인지 체크
            if len(year) != 4 or not year.isdigit():
                raise ValueError("연도는 4자리 숫자로 입력해야 합니다.")
            if len(month) != 2 or not month.isdigit() or not (1 <= int(month) <= 12):
                raise ValueError("월은 01에서 12 사이의 숫자로 입력해야 합니다.")
            if len(day) != 2 or not day.isdigit() or not (1 <= int(day) <= 31):
                raise ValueError("일은 01에서 31 사이의 숫자로 입력해야 합니다.")
            
            if len(hour) != 2 or not hour.isdigit() or not (0 <= int(hour) <= 23):
                raise ValueError("시간은 00에서 23 사이의 숫자로 입력해야 합니다.")
            if len(minu) != 2 or not minu.isdigit() or not (0 <= int(minu) <= 59):
                raise ValueError("분은 00에서 59 사이의 숫자로 입력해야 합니다.")     
            NOW = f'{year}-{month}-{day} {hour}:{minu}'
            
        except ValueError as e:
            print(f"입력 오류: {e}")
            return
        except Exception as e:
            print("알 수 없는 오류가 발생했습니다.")
            return
        
        log_entry = f'================= {NOW} ================= \n' \
                    f'화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']}°C, \n' \
                    f'화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']}°C, \n' \
                    f'화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']}%, \n' \
                    f'화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']} W/m², \n' \
                    f'화성 기지 내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']}%, \n' \
                    f'화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']}%'
        
        try:
            with open(LOG_FILE_PATH, 'w', encoding='UTF-8') as file:
                file.write(log_entry)
        except Exception as e:
            print(f'Unexpected error: {e}')
            return
        
        # 로그 내용 반환 (디버깅이나 다른 용도로)
        return self.env_values    

ds = DummySensor()
ds.set_env()
print(ds.get_env())
