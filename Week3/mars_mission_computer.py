import random

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
        return self.env_values

ds = DummySensor()
ds.set_env()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
print(ds.get_env())