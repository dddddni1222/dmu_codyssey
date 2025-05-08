from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from decimal import Decimal, InvalidOperation
import sys

class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = "0"
        self.previous = None
        self.operator = None
        self.new_input = True
        self.display_state = None

    def add(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b

    def subtract(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b

    def multiply(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b

    def divide(self, a: Decimal, b: Decimal) -> Decimal:
        return a / b if b != 0 else Decimal('inf')

    def percent(self):
        try:
            self.current = str(Decimal(self.current) / 100)
            self.display_state = None
        except InvalidOperation:
            self.current = "Error"
            self.reset()

    def negative_positive(self):
        try:
            if self.current and self.current != "0":
                self.current = self.current[1:] if self.current.startswith('-') else '-' + self.current
            self.display_state = None
        except:
            self.current = "Error"
            self.reset()

    def input_number(self, number: str):
        if len(self.current) >= 16 and not self.new_input: return
        if self.new_input or self.current == "0":
            self.current = number
            self.new_input = False
        else:
            self.current += number
        self.display_state = None

    def input_decimal(self):
        if '.' not in self.current and not self.new_input:
            self.current += '.'
        self.display_state = None

    def backspace(self):
        if self.current != "0":
            self.current = self.current[:-1] or "0"
            self.new_input = False
        self.display_state = None

    def set_operator(self, op: str):
        try:
            if self.previous is None:
                self.previous = Decimal(self.current)
                self.display_state = f"{self.current} {op}"
            elif not self.new_input:
                self.equal()
                self.display_state = f"{self.current} {op}"
            self.operator = op
            self.new_input = True
        except InvalidOperation:
            self.current = "Error"
            self.reset()

    def equal(self):
        try:
            if self.previous is not None and self.operator:
                ops = {'+': self.add, '-': self.subtract, '×': self.multiply, '÷': self.divide, '%': lambda x, y: x % y if y != 0 else Decimal('inf')}
                result = ops[self.operator](Decimal(self.previous), Decimal(self.current))
                if result == Decimal('inf'):
                    self.current = "Error"
                else:
                    result = result.quantize(Decimal('0.000001'), rounding='ROUND_HALF_UP')
                    self.current = str(result).rstrip('0').rstrip('.') if len(str(result)) <= 16 else "Too Large"
                self.previous = Decimal(self.current) if self.current not in ["Error", "Too Large"] else None
                self.operator = None
                self.new_input = True
                self.display_state = None
        except InvalidOperation:
            self.current = "Error"
            self.reset()

    def get_display(self):
        return self.display_state or ("Too Large" if len(self.current) > 16 else self.current) if self.current != "Error" else "Error"

    def get_font_size(self):
        return 48 if len(self.get_display()) <= 8 else 36 if len(self.get_display()) <= 12 else 28

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(360, 580)
        self.setStyleSheet("background-color: #1C1C1C;")
        self.calculator = Calculator()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("background-color: #1C1C1C; color: white; border: none; padding: 20px; font-size: 48px;")
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [('AC', 'func'), ('+/-', 'func'), ('%', 'op'), ('÷', 'op'),
                   ('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'op'),
                   ('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'op'),
                   ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'),
                   ('←', 'func'), ('0', 'num'), ('.', 'num'), ('=', 'op')]

        styles = {'num': "background-color: #505050;", 'op': "background-color: #FF9500;", 'func': "background-color: #A5A5A5;"}

        for i, (val, typ) in enumerate(buttons):
            btn = QPushButton(val)
            btn.setFixedSize(80, 80)
            font_size = 40 if val in ['+', '-', '×', '÷', '='] else 30
            btn.setStyleSheet(f"{styles[typ]} color: white; border-radius: 40px; font-size: {font_size}px;")
            btn.clicked.connect(self.button_clicked)
            grid.addWidget(btn, i // 4, i % 4)

        layout.addLayout(grid)
        self.setLayout(layout)

    def button_clicked(self):
        text = self.sender().text()
        if self.calculator.current == "Error" and text != 'AC': return

        actions = {
            '0': lambda: self.calculator.input_number('0'),
            '1': lambda: self.calculator.input_number('1'),
            '2': lambda: self.calculator.input_number('2'),
            '3': lambda: self.calculator.input_number('3'),
            '4': lambda: self.calculator.input_number('4'),
            '5': lambda: self.calculator.input_number('5'),
            '6': lambda: self.calculator.input_number('6'),
            '7': lambda: self.calculator.input_number('7'),
            '8': lambda: self.calculator.input_number('8'),
            '9': lambda: self.calculator.input_number('9'),
            '.': self.calculator.input_decimal,
            '+': lambda: self.calculator.set_operator('+'),
            '-': lambda: self.calculator.set_operator('-'),
            '×': lambda: self.calculator.set_operator('×'),
            '÷': lambda: self.calculator.set_operator('÷'),
            '%': lambda: self.calculator.set_operator('%'),
            '=': self.calculator.equal,
            'AC': self.calculator.reset,
            '+/-': self.calculator.negative_positive,
            '←': self.calculator.backspace
        }
        actions.get(text, lambda: None)()

        self.display.setText(self.calculator.get_display())
        self.display.setStyleSheet(f"background-color: #1C1C1C; color: white; border: none; padding: 20px; font-size: {self.calculator.get_font_size()}px;")

    def keyPressEvent(self, event):
        if self.calculator.current == "Error" and event.text() != 'AC': return

        key_map = {
            Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3', Qt.Key_4: '4',
            Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7', Qt.Key_8: '8', Qt.Key_9: '9',
            Qt.Key_Period: '.', Qt.Key_Plus: '+', Qt.Key_Minus: '-', Qt.Key_Asterisk: '×',
            Qt.Key_Slash: '÷', Qt.Key_Percent: '%', Qt.Key_Enter: '=', Qt.Key_Return: '=',
            Qt.Key_Escape: 'AC', Qt.Key_Backspace: '←', Qt.Key_PlusMinus: '+/-'
        }
        text = key_map.get(event.key())
        if text:
            actions = {
                '0': lambda: self.calculator.input_number('0'),
                '1': lambda: self.calculator.input_number('1'),
                '2': lambda: self.calculator.input_number('2'),
                '3': lambda: self.calculator.input_number('3'),
                '4': lambda: self.calculator.input_number('4'),
                '5': lambda: self.calculator.input_number('5'),
                '6': lambda: self.calculator.input_number('6'),
                '7': lambda: self.calculator.input_number('7'),
                '8': lambda: self.calculator.input_number('8'),
                '9': lambda: self.calculator.input_number('9'),
                '.': self.calculator.input_decimal,
                '+': lambda: self.calculator.set_operator('+'),
                '-': lambda: self.calculator.set_operator('-'),
                '×': lambda: self.calculator.set_operator('×'),
                '÷': lambda: self.calculator.set_operator('÷'),
                '%': lambda: self.calculator.set_operator('%'),
                '=': self.calculator.equal,
                'AC': self.calculator.reset,
                '+/-': self.calculator.negative_positive,
                '←': self.calculator.backspace
            }
            actions.get(text, lambda: None)()

            self.display.setText(self.calculator.get_display())
            self.display.setStyleSheet(f"background-color: #1C1C1C; color: white; border: none; padding: 20px; font-size: {self.calculator.get_font_size()}px;")

def create_calculator_ui():
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    create_calculator_ui()
