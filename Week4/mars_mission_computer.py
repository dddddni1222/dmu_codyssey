import time
import random

class MissionComputer:
    def __init__(self, use_dummy_sensor=False):
        self.env_values = { 
            key: 0.0 for key in [
                'mars_base_internal_temperature', 'mars_base_external_temperature',
                'mars_base_internal_humidity', 'mars_base_external_illuminance',
                'mars_base_internal_co2', 'mars_base_internal_oxygen'
            ]
        }
        self.running = True
        self.data_history = []
        self.ds = DummySensor() if use_dummy_sensor else None

    def get_valid_input(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == 'q':
                self.running = False
                return None
            try:
                return float(user_input)
            except ValueError:
                print("숫자 값을 입력해주세요.")

    def update_env_values(self):
        if self.ds:
            self.env_values.update(self.ds.get_env())
        else:
            for key in self.env_values.keys():
                value = self.get_valid_input(f'{key.replace("_", " ").title()} : ')
                if value is None:
                    return False
                self.env_values[key] = value
        return True

    def format_env_values(self):
        return "{\n" + "\n".join(f'  "{k}": {round(v, 2)}' for k, v in self.env_values.items()) + "\n}"

    def print_5_min_average(self):
        if not self.data_history:
            print("\n5-Minute Average Data: No data available yet.")
            return

        avg_values = {key: sum(d[key] for d in self.data_history[-60:]) / min(len(self.data_history), 60) for key in self.env_values}
        print("\n5-Minute Average Data:\n{\n" + "\n".join(f'  "{k}": {round(v, 2)}' for k, v in avg_values.items()) + "\n}")

    def run(self):
        last_5_min_check_time = time.time()

        while self.running:
            if not self.update_env_values():
                print("System stopped....")
                break

            self.data_history.append(self.env_values.copy())
            print(self.format_env_values())

            if time.time() - last_5_min_check_time >= 30:
                self.print_5_min_average()
                last_5_min_check_time = time.time()

            time.sleep(5) 

class DummySensor:
    def __init__(self):
        self.env_ranges = {
            'mars_base_internal_temperature': (18, 30), 'mars_base_external_temperature': (0, 21),
            'mars_base_internal_humidity': (50, 60), 'mars_base_external_illuminance': (500, 715),
            'mars_base_internal_co2': (0.02, 0.1), 'mars_base_internal_oxygen': (4, 7)
        }

    def get_env(self):
        """랜덤 환경 변수 값 반환"""
        return {key: round(random.uniform(*range_), 2) for key, range_ in self.env_ranges.items()}

if __name__ == '__main__':
    try:
        use_dummy = input("더미 센서를 사용할까요? (y/n): ").strip().lower() == 'y'
        MissionComputer(use_dummy_sensor=use_dummy).run()
    except KeyboardInterrupt:
        print("Sytem stoped….")
