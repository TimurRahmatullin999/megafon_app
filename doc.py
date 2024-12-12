# self.setFixedSize(QSize(400, 300)) - фиксированное окно
# self.setCentralWidget(button) - задать кнопку по центру
# setChecked() - метод стартового нажатия кнопки, если внутри True, то кнопка нажата, если нет то False
# isChecked() - метод проверяет нажата ли сейчас кнопка или нет, если да то True, если нет то False
# clicked - метод отжатия нажатия кнопки
# released - метод отжатия кнопки
# setCheckable - Когда вы устанавливаете элемент как "checkable" (можно выбрать), это означает, что он может находиться в двух состояниях: активном (выбранном) и неактивном (невыбранном).
# windowTitleChanged.connect - метод вызываемый при изменении имени приложения
# self.button.setDisabled(True) - отключает работоспособность кнопки, аналогичен self.button.Enable(False)

'''
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow

import sys
from random import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.setWindowTitle("My App")
        self.button = QPushButton("Войти")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Нажато")
        new_title_window = choice(window_titles)
        print("Setting title:  %s" % new_title_window)
        self.setWindowTitle(new_title_window)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
'''

# QLabel() - метод создающий текстовую метку в приложении
# QLineEdit() - метод создающий вводимое текстовое поле
'''self.lineedit.textChanged.connect(self.label.setText) - метод связывающий вводимое поле и текстовую метка
при данном коннекте меняется тектовая метка при вводе символов в текстовое поле'''
# self.layout = QVBoxLayout() - создание вертикального виджета
# self.layout.addWidget(self.input)
#  self.layout.addWidget(self.label) - добавление вертикальных виджетов
#  container = QWidget()
#  container.setLayout(self.layout) - подключение вертикального виджета к основному виджету
# self.input_password.setPlaceholderText("Введите пароль") - задает информацию по вкладке при отсутствии введенного текста
# self.input_password.setEchoMode(QLineEdit.EchoMode.Password) - скрывает вводимый текст
# self.input_password.setEchoMode(QLineEdit.EchoMode.Normal) - не скрывает вводимый текст