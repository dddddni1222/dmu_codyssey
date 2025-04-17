def create_calculator_ui():
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
    from PyQt5.QtCore import Qt, QSize
    from PyQt5.QtGui import QIcon

    class CalculatorUI(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("iPhone Style Calculator")
            self.setFixedSize(360, 580)
            self.setStyleSheet("background-color: #1C1C1C;")
            self.initUI()

        def initUI(self):
            main_layout = QVBoxLayout()

            # 출력창
            self.display = QLineEdit()
            self.display.setText("0")
            self.display.setReadOnly(True)
            self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
            self.display.setFixedHeight(100)
            self.display.setStyleSheet("""
                background-color: #1C1C1C;
                color: white;
                font-size: 48px;
                border: none;
                padding: 20px 20px 2px 20px;
            """)
            main_layout.addWidget(self.display)

            # 버튼 레이아웃
            button_layout = QGridLayout()

            buttons = [
                ['AC', '+/-', '%', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['←', '0', '.', '=']
            ]

            styles = {
                'num': "background-color: #505050; color: white; font-weight: bold;",
                'op': "background-color: #FF9500; color: white; font-weight: bold;",
                'func': "background-color: #A5A5A5; color: white; font-weight: bold;"
            }

            for row, row_values in enumerate(buttons):
                for col, value in enumerate(row_values):
                    btn = QPushButton(value)
                    btn.setFixedHeight(80)

                    if value == '←':
                        btn.setFixedWidth(80)
                        button_layout.addWidget(btn, row + 1, col)
                    elif value == '0':
                        btn.setFixedWidth(80)  
                        button_layout.addWidget(btn, row + 1, 1)
                    elif value == '.':
                        btn.setFixedWidth(80)
                        button_layout.addWidget(btn, row + 1, 2) 
                    elif value == '=':
                        btn.setFixedWidth(80)
                        button_layout.addWidget(btn, row + 1, 3)
                    else:
                        btn.setFixedWidth(80)
                        button_layout.addWidget(btn, row + 1, col)

                    if value in ['+', '-', '×', '÷', '=']:
                        btn.setStyleSheet(f"""
                            {styles['op']}
                            border-radius: 40px;
                            font-size: 40px;
                        """)
                    elif value in ['AC', '+/-', '%']:
                        btn.setStyleSheet(f"""
                            {styles['func']}
                            border-radius: 40px;
                            font-size: 30px;
                        """)
                    else:
                        btn.setStyleSheet(f"""
                            {styles['num']}
                            border-radius: 40px;
                            font-size: 30px;
                        """)

                    btn.clicked.connect(self.button_clicked)

            main_layout.addLayout(button_layout)
            self.setLayout(main_layout)

        def button_clicked(self):
            sender = self.sender()
            text = sender.text()
            current = self.display.text().replace(",", "")  # 쉼표 제거

            def format_number_parts(expr):
                ops = ['+', '-', '×', '÷', '%']
                last_op_index = -1

                # 1. 맨 앞 '-'는 부호이므로 스킵
                for i in range(len(expr) - 1, 0, -1):
                    if expr[i] in ops:
                        last_op_index = i
                        break

                if last_op_index == -1:
                    # 전체가 숫자일 경우
                    try:
                        if '.' in expr:
                            return f"{float(expr):,}"
                        else:
                            return f"{int(expr):,}"
                    except:
                        return expr

                front_number = expr[:last_op_index]
                operator = expr[last_op_index]
                back_number = expr[last_op_index + 1:]

                # 앞 숫자 포맷
                try:
                    if '.' in front_number:
                        front_number = f"{float(front_number):,}"
                    else:
                        front_number = f"{int(front_number):,}"
                except:
                    pass

                # 뒤 숫자 포맷
                try:
                    if '.' in back_number:
                        back_number = f"{float(back_number):,}"
                    elif back_number:
                        back_number = f"{int(back_number):,}"
                except:
                    pass

                return front_number + operator + back_number

            if text in '0123456789':
                if current == "0":
                    current = text
                else:
                    current += text
                self.display.setText(format_number_parts(current))

            elif text == '.':
                # 마지막 숫자에만 소수점 허용
                last_part = current.split('+')[-1].split('-')[-1].split('×')[-1].split('÷')[-1].split('%')[-1]
                if '.' not in last_part:
                    current += '.'
                self.display.setText(current)

            elif text in '+-×÷%':
                if current[-1] in '+-×÷%':
                    return
                current += text
                self.display.setText(format_number_parts(current))

            elif text == '=':
                expression = self.display.text().replace(",", "").replace('×', '*').replace('÷', '/')
                try:
                    expression = expression.replace('%', '/100')
                    result = eval(expression)
                    if isinstance(result, float):
                        result = f"{result:,.7f}"
                    else:
                        result = f"{result:,}"
                    self.display.setText(result)
                except Exception:
                    self.display.setText("Error")

            elif text == 'AC':
                self.display.setText("0")

            elif text == '+/-':
                if current.startswith('-'):
                    current = current[1:]
                elif current != "0":
                    current = '-' + current
                self.display.setText(format_number_parts(current))

            elif text == '←':
                if len(current) > 1:
                    current = current[:-1]
                else:
                    current = "0"
                self.display.setText(format_number_parts(current))



    app = QApplication([])
    window = CalculatorUI()
    window.show()
    app.exec_()

create_calculator_ui()
