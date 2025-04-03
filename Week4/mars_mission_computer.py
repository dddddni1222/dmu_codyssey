import time

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.running = True
        self.data_history = []

    def get_valid_input(self, prompt):
        """입력값 검증 및 'q' 체크"""
        user_input = input(prompt).strip()
        if user_input.lower() == 'q':
            self.running = False
            return None
        if not user_input:
            print("입력 값이 비어 있습니다. 다시 입력해주세요.")
            return self.get_valid_input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("숫자 값을 입력해주세요.")
            return self.get_valid_input(prompt)

    def set_env(self):
        """환경 값 입력"""
        for key in self.env_values.keys():
            value = self.get_valid_input(f'{key.replace("_", " ").title()} : ')
            if value is None:  # 'q' 입력 시 종료
                return False
            self.env_values[key] = value
        return True

    def get_sensor_data(self):
        """5초마다 데이터 갱신 및 출력, 5분마다 평균 출력"""
        last_check_time = time.time()
        last_5_min_check_time = time.time()

        while self.running:
            current_time = time.time()

            if current_time - last_check_time >= 5:
                if not self.set_env():  # 'q' 입력 시 종료
                    print("System stopped....")
                    break
                last_check_time = current_time

                # JSON 출력
                json_output = "{\n"
                for key, value in self.env_values.items():
                    json_output += f'"{key}": {round(value, 2)},\n'
                json_output = json_output.rstrip(',\n') + "\n"
                json_output += "}"
                print(json_output)

                self.data_history.append(self.env_values.copy())

            if current_time - last_5_min_check_time >= 300:  # 5분
                self.print_5_min_average()
                last_5_min_check_time = current_time

            time.sleep(1)

    def print_5_min_average(self):
        """5분 평균 출력"""
        if not self.data_history:
            print("\n5-Minute Average Data: No data available yet.")
            return

        avg_values = {key: 0 for key in self.env_values.keys()}
        data_count = min(len(self.data_history), 60)

        for data in self.data_history[-data_count:]:
            for key, value in data.items():
                avg_values[key] += value

        print("\n5-Minute Average Data:")
        for key, value in avg_values.items():
            print(f'  {key}: {round(value / data_count, 2)}')
        print("\n")

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
        
        log_entry = f'화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']}°C, \n' \
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
        
        # 로그 내용 반환 (디버깅이나 다른 용도로)
        return self.env_values    

if __name__ == '__main__':
    ds = DummySensor()
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()