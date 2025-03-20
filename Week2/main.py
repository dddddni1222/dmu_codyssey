# 상수 정의
FILE_DO_ERROR = '파일 처리 중 오류 발생했습니다.'
FILE_DECODE_ERROR = '파일 디코딩 중 오류 발생했습니다.'
FILE_NOT_FOUND_ERROR = '파일을 찾을 수 없습니다.'
FILE_PRINT = '=============================== 파일출력 ==============================='
CSV_READ_ERROR = 'CSV 파일을 읽는 데 실패했습니다'
UNKNOWN_ERROR = '알 수 없는 오류가 발생했습니다'

def get_file():
    sample_path = r'C:\Users\YourUsername\Desktop\Mars_Base_Inventory_List.csv'

    file_path = input(f'불러 올 파일의 경로를 입력해 주세요. (예시: {sample_path}): ').strip('"')

    return file_path

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'{FILE_NOT_FOUND_ERROR}: {file_path}')
        return None

def get_filepath(file_path):
    last_slash_index = file_path.rfind('\\')
    if last_slash_index == -1:
        return file_path  
    return file_path[:last_slash_index]

def read_csv_to_list(filename):
    data_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                row = [item.strip() for item in line.split(',')] 
                data_list.append(row)
    except FileNotFoundError:
        print(f'{FILE_NOT_FOUND_ERROR}: {filename}')
    return data_list

def get_Flammability(data):
    for idx, item in enumerate(data[0]):
        if item == 'Flammability':
            return idx
    return None

def sort_Flammability(data, idx, reverse=False):
    first_row = data[0]
    rest_of_data = data[1:]

    rest_of_data.sort(key=lambda x: x[idx], reverse=reverse)
    sorted_data = [first_row] + rest_of_data

    return sorted_data

def filter_Flammability(data, idx, value):
    first_row = data[0]

    filtered_data = [first_row]
    for item in data[1:]:
        try:
            number = float(item[idx])
            if number >= value:
                filtered_data.append(item)
        except ValueError:
            continue
    
    return filtered_data

def save_csvfile(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            for i, row in enumerate(data):
                if i < len(data) - 1:
                    file.write(','.join(map(str, row)) + '\n')
                else:
                    file.write(','.join(map(str, row)))
    except IOError as e:
        print(f'{FILE_DO_ERROR}: {e}')

def save_binfile(data, filename):
    try:
        with open(filename, 'wb') as file:
            for row in data:
                for item in row:
                    file.write(item.encode('utf-8') + b'\0')
    except IOError as e:
        print(f'{FILE_DO_ERROR}: {e}')

def read_bin(filename):
    try:
        with open(filename, 'rb') as file:
            byte_data = file.read()
            
            strings = byte_data.split(b'\0') 
            
            decoded_strings = []
            for item in strings:
                if item: 
                    try:
                        decoded_strings.append(item.decode('utf-8'))  
                    except UnicodeDecodeError as e:
                        print(f'{FILE_DECODE_ERROR}: {e}')
            
            # 5개씩 묶어서 이차원 배열로 저장
            result = [decoded_strings[i:i+5] for i in range(0, len(decoded_strings), 5)]

        return result
    except IOError as e:
        print(f'{FILE_DO_ERROR}: {e}')
        return []

def main():
    try:
        # 1. Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력한다. 
        file_path = get_file()
        if file_path is None:
            return

        log_data = read_file(file_path)
        if log_data is None:
            return

        print(f'{FILE_PRINT} : \n{log_data}')
        
        file_dir = get_filepath(file_path)
        SAVECSV = file_dir + r'\Mars_Base_Inventory_danger.csv'
        SAVEBIN = file_dir + r'\Mars_Base_Inventory_List.bin'

        # 2. Mars_Base_Inventory_List.csv 내용을 읽어서 Python의 리스트(List) 객체로 변환한다.
        list_data = read_csv_to_list(file_path)
        if not list_data:
            print(f'{CSV_READ_ERROR}')
            return

        idx = get_Flammability(list_data)
        if idx is None:
            print("'Flammability' 열을 찾을 수 없습니다.")
            return

        # 3. 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬한다.
        list_sort = sort_Flammability(list_data, idx, True)

        # 4. 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력한다. 
        VALUE = 0.7
        list_danger = filter_Flammability(list_sort, idx, VALUE)
        print(f'===============================인화성 지수가 {VALUE} 이상인 리스트 ===============================: \n{list_danger}')

        # 5. 인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장한다.
        save_csvfile(list_danger, SAVECSV)

        # B-1. 인화성 순서로 정렬된 배열의 내용을 이진 파일형태로 저장한다.
        save_binfile(list_danger, SAVEBIN)

        # B-2. 저장된 Mars_Base_Inventory_List.bin 의 내용을 다시 읽어 들여서 화면에 내용을 출력한다.
        list_bin = read_bin(SAVEBIN)
        print(f'{FILE_PRINT} : \n{list_bin}')

    except Exception as e:
        print(f'{UNKNOWN_ERROR}: {e}')

if __name__ == '__main__':
    main()
