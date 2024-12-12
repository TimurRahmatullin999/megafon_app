import sys
import sqlite3
from datetime import date, timedelta
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, \
    QHBoxLayout, QMessageBox, QTextBrowser, QStackedLayout, QFrame, QProgressBar


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.user = []

        self.setWindowTitle("Приложение Мегафон")
        self.setGeometry(0, 0, 0, 0)
        self.setMinimumSize(1400, 1080)

        # Создаем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Виджет авторизации пользователя
        self.widget_login = QWidget()
        self.setup_login()

        # Виджет тарифов
        self.widget_tariffs = QWidget()

        # Виджет услуг
        self.widget_services = QWidget()


        # Виджет меню личного кабинета
        self.widget_menu = QWidget()


        self.info_profile = QWidget()

        self.widget_my_tariff = QWidget()

        self.widget_my_service = QWidget()

        self.widget_balance = QWidget()

        self.main_layout.addWidget(self.widget_login)

    def setup_login(self):
        self.password_h = QHBoxLayout()

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedWidth(250)
        self.input_password.setFixedHeight(30)

        self.input_password.setStyleSheet("""
                                            QLineEdit {
                                                border: 0.5px solid black;
                                                border-radius: 5px;
                                            }
                                """)

        self.button_password = QPushButton("Показать")
        self.button_password.setCheckable(True)
        self.button_password.clicked.connect(self.clicked_button_password)
        self.button_password.setFixedWidth(80)
        self.button_password.setFixedHeight(25)

        self.password_h.addStretch()
        self.password_h.addWidget(self.input_password, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.password_h.addWidget(self.button_password, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.password_h.addStretch()

        self.button = QPushButton("Войти")
        self.button.clicked.connect(self.verificate_user)
        self.button.setFixedWidth(100)

        self.button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CAF50;
                                        color: white;
                                        border: none;
                                        padding: 10px 20px;
                                        font-size: 16px;
                                        border-radius: 15px;
                                    }
                                    QPushButton:hover {
                                        background-color: #45a049;
                                    }
                                    QPushButton:pressed {
                                        background-color: #3e8e41;
                                    }
                                """)

        self.input_number = QLineEdit()
        self.input_number.setPlaceholderText("Введите номер телефона")

        self.input_number.setStyleSheet("""
                                    QLineEdit {
                                        border: 0.5px solid black;
                                        border-radius: 5px;
                                    }
                        """)

        self.input_number.setFixedWidth(250)
        self.input_number.setFixedHeight(30)

        self.login_user = QVBoxLayout()
        self.login_user.addStretch()
        self.login_user.addWidget(self.input_number, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.login_user.addLayout(self.password_h)
        self.login_user.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.login_user.addStretch()

        self.widget_login.setLayout(self.login_user)

    def clicked_button_password(self):
        if self.button_password.isChecked():
            print("Пароль видно")
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.button_password.setText("Скрыть")
        else:
            print("Пароль скрыт")
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.button_password.setText("Показать")

    def verificate_user(self):

        phone_number = self.input_number.text()
        password = self.input_password.text()

        container = sqlite3.connect('Users.db')
        cursor = container.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_phone_number=? AND user_password=?", (phone_number, password))

        self.user = cursor.fetchall()
        cursor.close()
        container.close()

        if self.user:
            QMessageBox.information(self, "Верно", "Вы успешно авторизовались")
            print("Данные введены верно")

            self.widget_login.hide()
            self.main_layout.addWidget(self.widget_menu)
            self.widget_menu.show()
            self.load_tariffs()
            self.main_menu_user()
            self.load_service()
            self.load_profile()

        else:
            QMessageBox.warning(self, "Ошибка", "Данные введены неверно, попробуйте авторизоваться еще раз")
            print("Данные введены неверно")

    def main_menu_user(self):
        self.main_menu = QVBoxLayout()

        # Создание виджета для верхнего фона
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: green;")
        header_widget.setFixedHeight(55)

        header_buttons = QHBoxLayout()

        button_tariff = QPushButton("Тарифы")
        button_tariff.clicked.connect(self.load_tariffs)
        button_tariff.clicked.connect(self.show_tariffs)

        button_service = QPushButton("Услуги")
        button_service.clicked.connect(self.load_service)
        button_service.clicked.connect(self.show_service)

        button_my_tariff = QPushButton("Мой тариф")
        button_my_tariff.clicked.connect(self.my_tariff)
        button_my_tariff.clicked.connect(self.show_my_tariff)
        button_my_tariff.setStyleSheet("""
                    QPushButton {
                        background-color: #D3D3D3;
                        color: black;
                        border: none;
                        padding: 10px 20px;
                        font-size: 11px;
                        border-radius: 5px;
                    }
                """)
        button_my_service = QPushButton("Мои услуги")
        button_my_service.clicked.connect(self.my_services)
        button_my_service.clicked.connect(self.show_my_service)
        button_my_service.setStyleSheet("""
                            QPushButton {
                                background-color: #D3D3D3;
                                color: black;
                                border: none;
                                padding: 10px 20px;
                                font-size: 11px;
                                border-radius: 5px;
                            }
                        """)

        button_balance = QPushButton("Баланс")
        button_balance.setStyleSheet("""
                                    QPushButton {
                                        background-color: #D3D3D3;
                                        color: black;
                                        border: none;
                                        padding: 10px 20px;
                                        font-size: 11px;
                                        border-radius: 5px;
                                    }
                                """)
        button_balance.clicked.connect(self.rephil_balance)
        button_balance.clicked.connect(self.show_bal_am)

        button_prof = QPushButton("Профиль")
        button_prof.clicked.connect(self.load_profile)
        button_prof.clicked.connect(self.show_profile)
        button_prof.setStyleSheet("""
            QPushButton {
                background-color: #D3D3D3;
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 11px;
                border-radius: 5px;
            }
        """)
        button_tariff.setStyleSheet("""
            QPushButton {
                background-color: #D3D3D3;
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 11px;
                border-radius: 5px;
            }
        """)
        button_prof.setFixedHeight(35)
        button_prof.setFixedWidth(150)

        button_service.setStyleSheet("""
                    QPushButton {
                        background-color: #D3D3D3;
                        color: black;
                        border: none;
                        padding: 10px 20px;
                        font-size: 11px;
                        border-radius: 5px;
                    }
                """)

        header_buttons.addStretch()
        header_buttons.addWidget(button_tariff, alignment=Qt.AlignmentFlag.AlignRight)
        header_buttons.addStretch()
        header_buttons.addWidget(button_service, alignment=Qt.AlignmentFlag.AlignRight)
        header_buttons.addStretch()
        header_buttons.addWidget(button_my_tariff, alignment=Qt.AlignmentFlag.AlignRight)
        header_buttons.addStretch()
        header_buttons.addWidget(button_my_service, alignment=Qt.AlignmentFlag.AlignRight)
        header_buttons.addStretch()
        header_buttons.addWidget(button_balance, alignment=Qt.AlignmentFlag.AlignRight)
        header_buttons.addStretch()
        header_buttons.addWidget(button_prof, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_widget.setLayout(header_buttons)

        self.main_menu.addWidget(header_widget)

        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, id_tariff, id_user, date_connected, date_written_of, remainder_internet, remainder_sms, remainder_minutes FROM Connected_tariffs WHERE id_user=?", (self.user[0][0],))
        connected_tariff = cursor.fetchall()
        cursor.execute("SELECT id, Title, Internet, Minutes, Sms, Price FROM Tariffs WHERE id=?", (connected_tariff[0][1],))
        info_tariff = cursor.fetchall()

        cursor.execute("SELECT id, id_service, id_user, date_written_off, remainder FROM Connected_services WHERE id_user=?", (self.user[0][0],))
        connected_service = cursor.fetchall()

        info_about_services = []
        for serv in connected_service:
            cursor.execute("SELECT id, title, type_of_service, price, value FROM Services WHERE id=?", (serv[1],))
            res = cursor.fetchall()
            info_about_services.append(res[0])

        value_internet_max = float(info_tariff[0][2]) + sum([float(i[4]) for i in info_about_services if i[2] == "Интернет" and not connected_service[info_about_services.index(i)][4] is None])
        current_internet = float(connected_tariff[0][5]) + sum([float(connected_service[info_about_services.index(i)][4]) for i in info_about_services if i[2] == "Интернет" and not connected_service[info_about_services.index(i)][4] is None])

        value_sms_max = int(info_tariff[0][4]) + sum([int(i[4]) for i in info_about_services if i[2] == "Сообщения" and not connected_service[info_about_services.index(i)][4] is None])
        current_sms = int(connected_tariff[0][6]) + sum([int(connected_service[info_about_services.index(i)][4]) for i in info_about_services if i[2] == "Сообщения" and not connected_service[info_about_services.index(i)][4] is None])

        value_minutes_max = int(info_tariff[0][3]) + sum([int(i[4]) for i in info_about_services if i[2] == "Звонки" and not connected_service[info_about_services.index(i)][4] is None])
        current_minutes = int(connected_tariff[0][7]) + sum([int(connected_service[info_about_services.index(i)][4]) for i in info_about_services if i[2] == "Звонки" and not connected_service[info_about_services.index(i)][4] is None])

        main_phon_widget = QWidget()
        main_phon_widget.setStyleSheet('background-color: #f2f2f2;')

        widget_tar_service = QVBoxLayout(main_phon_widget)
        info_name_price = QHBoxLayout()
        frame_layout = QHBoxLayout()
        title_label = QLabel('Мой тариф')
        title_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        info_about_payment = QLabel(str(connected_tariff[0][4]) + " спишется " + str(info_tariff[0][5]) + " ₽")
        info_about_payment.setStyleSheet("color: black;")

        minutes_frame = self.create_msi("Минуты", current_minutes, value_minutes_max)
        frame_layout.addWidget(minutes_frame)

        internet_frame = self.create_msi("Интернет", current_internet, value_internet_max)
        frame_layout.addWidget(internet_frame)

        sms_frame = self.create_msi("SMS", current_sms, value_sms_max)
        frame_layout.addWidget(sms_frame)

        info_name_price.addStretch()
        info_name_price.addWidget(title_label, alignment = Qt.AlignmentFlag.AlignHCenter)
        info_name_price.addSpacing(20)
        info_name_price.addWidget(info_about_payment, alignment = Qt.AlignmentFlag.AlignHCenter)
        info_name_price.addStretch()
        widget_tar_service.addLayout(info_name_price)
        widget_tar_service.addLayout(frame_layout)
        widget_tar_service.addStretch()
        self.main_menu.addWidget(main_phon_widget)

        self.widget_menu.setLayout(self.main_menu)


    def create_msi(self, title, value_ost, max_value):
        card = QFrame()
        card.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 10px;")
        card.setFixedHeight(200)
        card.setFixedWidth(400)

        layout_msi = QVBoxLayout(card)
        layout_msi.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel(str(title))
        title_label.setStyleSheet("font-weight: bold;")

        usage_label = QLabel(f"{round(value_ost,3)} из {max_value}")

        process_bar = QProgressBar()
        process_bar.setValue(int((value_ost/max_value)*100))
        process_bar.setTextVisible(False)
        if int((value_ost/max_value)*100) >= 60:
            process_bar.setStyleSheet("""
                        QProgressBar {
                            border: none;
                            background-color: #e0e0e0;
                            height: 10px;
                            border-radius: 5px;
                        }
                        QProgressBar::chunk {
                            background-color: #4caf50;
                            border-radius: 5px;
                        }
                    """)
        elif 20 <= int((value_ost/max_value)*100) <= 59:
            process_bar.setStyleSheet("""
                                    QProgressBar {
                                        border: none;
                                        background-color: #e0e0e0;
                                        height: 10px;
                                        border-radius: 5px;
                                    }
                                    QProgressBar::chunk {
                                        background-color: orange;
                                        border-radius: 5px;
                                    }
                                """)
        else:
            process_bar.setStyleSheet("""
                                    QProgressBar {
                                        border: none;
                                        background-color: #e0e0e0;
                                        height: 10px;
                                        border-radius: 5px;
                                    }
                                    QProgressBar::chunk {
                                        background-color: red;
                                        border-radius: 5px;
                                    }
                                """)

        layout_msi.addWidget(title_label)
        layout_msi.addWidget(usage_label)
        layout_msi.addWidget(process_bar)

        return card

    def my_tariff(self):
        self.layout_my_tariff = QVBoxLayout()

        frame_hv = QHBoxLayout()
        priced = QHBoxLayout()
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Connected_tariffs WHERE id_user=?", (self.user[0][0],))
        num_tariff = cursor.fetchall()
        print(num_tariff)
        cursor.execute("SELECT id, Title, Internet, Minutes, Sms, Price FROM Tariffs")
        all_tariffs = cursor.fetchall()
        all_tariffs = list(filter(lambda x: x[0] == num_tariff[0][1], all_tariffs))
        print(all_tariffs)
        named_tariff = QLabel(f"Мой тариф: {all_tariffs[0][1]}")
        named_tariff.setFont(QFont("Arial", 18))
        price_date = QLabel(str(num_tariff[0][4]) + " спишется " + str(all_tariffs[0][5]) + " ₽")
        priced.addStretch()
        priced.addWidget(named_tariff, alignment = Qt.AlignmentFlag.AlignHCenter)
        priced.setSpacing(10)
        priced.addWidget(price_date, alignment = Qt.AlignmentFlag.AlignHCenter)
        priced.addStretch()
        self.layout_my_tariff.addLayout(priced)
        frame_hv.addWidget(self.create_msi("Минуты", num_tariff[0][8], all_tariffs[0][3]))
        frame_hv.addWidget(self.create_msi("Интернет", num_tariff[0][6], all_tariffs[0][2]))
        frame_hv.addWidget(self.create_msi("SMS", num_tariff[0][7], all_tariffs[0][4]))
        self.layout_my_tariff.addLayout(frame_hv)
        self.layout_my_tariff.addStretch()
        buttons_hv = QHBoxLayout()
        back = QPushButton("Назад")
        back.clicked.connect(self.back_menu_from_my_tariff)
        back.setStyleSheet(
            "background-color: grey; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        change_tariff = QPushButton("Сменить тариф")
        change_tariff.clicked.connect(self.show_change)
        change_tariff.setStyleSheet(
            "background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        buttons_hv.addStretch()
        buttons_hv.addWidget(change_tariff, alignment = Qt.AlignmentFlag.AlignHCenter)
        buttons_hv.addWidget(back, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.layout_my_tariff.addLayout(buttons_hv)

        self.widget_my_tariff.setStyleSheet("background-color: #ddffec")
        self.widget_my_tariff.setLayout(self.layout_my_tariff)

    def my_services(self):
        services_layout = QVBoxLayout()
        service_1 = QLabel("Услуги")
        service_1.setFont(QFont("Arial", 18))
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title, type_of_service, description, price, type_of_written, text_for_written, value, url_tar FROM Services")
        result = cursor.fetchall()
        print(result)

        cursor.execute("SELECT id_service, id_user, date_written_off, remainder FROM Connected_services WHERE id_user=?", (self.user[0][0],))
        con_services = cursor.fetchall()
        print(con_services)
        aft_res = []
        for service in result:
            for one in con_services:
                if one[0] == service[0]:
                    aft_res.append(service)
        print(aft_res)
        con_services = sorted(con_services, key=lambda x: x[0])
        print(con_services)
        hv_services = QHBoxLayout()
        for j in range(len(aft_res)):
            card = QFrame()
            card.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 10px;")
            card.setFixedHeight(350)
            card.setFixedWidth(350)

            layout_msi = QVBoxLayout(card)
            layout_msi.setAlignment(Qt.AlignmentFlag.AlignTop)

            if aft_res[j][5] == "Одноразовое":
                date_written = QLabel(f"Списание не будет,\nуслуга действительна до\n{con_services[j][2]}")
            elif aft_res[j][5] == "Бессрочное":
                date_written = QLabel(f"Списание не будет, срок действия до {con_services[j][2]}")
            else:
                date_written = QLabel(f"{con_services[j][2]} списание {aft_res[j][4]} ₽")

            title_label = QLabel(aft_res[j][1])
            title_label.setStyleSheet("font-weight: bold;")
            layout_msi.addWidget(title_label)
            layout_msi.addWidget(date_written)
            title_usage_label = QLabel(aft_res[j][2])
            title_usage_label.setStyleSheet("font-weight: bold;")
            layout_msi.addWidget(title_usage_label)
            if not con_services[j][3] is None:
                print(con_services[j])
                usage_label = QLabel(f"{round(con_services[j][3], 3)} из {aft_res[j][7]}")
                process_bar = QProgressBar()
                process_bar.setValue(int((con_services[j][3] / aft_res[j][7]) * 100))
                process_bar.setTextVisible(False)
                if int((con_services[j][3] / aft_res[j][7]) * 100) >= 60:
                    process_bar.setStyleSheet("""
                                                            QProgressBar {
                                                                border: none;
                                                                background-color: #e0e0e0;
                                                                height: 10px;
                                                                border-radius: 5px;
                                                            }
                                                                QProgressBar::chunk {
                                                                background-color: #4caf50;
                                                                border-radius: 5px;
                                                            }
                                                        """)
                elif 20 <= int((con_services[j][3] / aft_res[j][7]) * 100) <= 59:
                    process_bar.setStyleSheet("""
                                                                        QProgressBar {
                                                                            border: none;
                                                                            background-color: #e0e0e0;
                                                                            height: 10px;
                                                                            border-radius: 5px;
                                                                        }
                                                                        QProgressBar::chunk {
                                                                            background-color: orange;
                                                                            border-radius: 5px;
                                                                        }
                                                                    """)
                else:
                    process_bar.setStyleSheet("""
                                                                        QProgressBar {
                                                                            border: none;
                                                                            background-color: #e0e0e0;
                                                                            height: 10px;
                                                                            border-radius: 5px;
                                                                        }
                                                                        QProgressBar::chunk {
                                                                            background-color: red;
                                                                            border-radius: 5px;
                                                                        }
                                                                    """)
                layout_msi.addWidget(usage_label)
                layout_msi.addWidget(process_bar)
            else:
                usage_label = QLabel(f"Тариф, в котором нет пакетов услуг")
                layout_msi.addWidget(usage_label)
            off_button =   QPushButton("Отключить")
            off_button.clicked.connect(partial(self.turn_off_service, aft_res[j]))
            off_button.setStyleSheet("background-color: red;")
            layout_msi.addStretch()
            layout_msi.addWidget(off_button, alignment = Qt.AlignmentFlag.AlignHCenter)
            hv_services.addWidget(card)
        services_layout.addWidget(service_1, alignment = Qt.AlignmentFlag.AlignHCenter)
        services_layout.addStretch()
        services_layout.addLayout(hv_services)
        services_layout.addStretch()
        back = QPushButton("Назад")
        back.setStyleSheet(
            "background-color: grey; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        back.clicked.connect(self.back_menu_from_my_services)
        services_layout.addWidget(back, alignment = Qt.AlignmentFlag.AlignRight)
        self.widget_my_service.setLayout(services_layout)


    def load_profile(self):
        self.profile = QVBoxLayout()

        pr = QWidget()
        pr.setStyleSheet("background-color: #ddffec; border-radius: 20px; font-family: Arial, sans-serif;")

        lk_2 = QVBoxLayout()

        lk = QVBoxLayout()
        low_buttons = QHBoxLayout()
        profile_card = QFrame()
        profile_card.setStyleSheet("background-color: white")


        start_words = QLabel("Ваши данные")
        number_phone = QLabel(f"Номер телефона: {self.user[0][1]}")
        name = QLabel(f"Имя: {self.user[0][3]}")
        surname = QLabel(f"Фамилия: {self.user[0][4]}")
        patronymic = QLabel(f"Отчество: {self.user[0][5]}")
        birthdate = QLabel(f"Дата рождения: {self.user[0][6]}")
        back = QPushButton("Назад")
        back.setFixedWidth(100)
        back.setFixedHeight(40)
        back.setStyleSheet(
            "background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        back.clicked.connect(self.back_menu_from_profile)
        quit = QPushButton("Выйти")
        quit.setFixedWidth(100)
        quit.setFixedHeight(40)
        quit.setStyleSheet(
            "background-color: red; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        quit.clicked.connect(self.quit_lk)

        lk_2.addWidget(start_words, alignment = Qt.AlignmentFlag.AlignHCenter)
        start_words.setFont(QFont("Arial", 18))
        lk.addWidget(number_phone)
        number_phone.setFont(QFont("Arial", 15))
        lk.addWidget(name)
        name.setFont(QFont("Arial", 15))
        lk.addWidget(surname)
        surname.setFont(QFont("Arial", 15))
        lk.addWidget(patronymic)
        patronymic.setFont(QFont("Arial", 15))
        lk.addWidget(birthdate)
        birthdate.setFont(QFont("Arial", 15))
        lk.addStretch()
        low_buttons.addStretch()
        low_buttons.addWidget(back, alignment = Qt.AlignmentFlag.AlignRight)
        low_buttons.addSpacing(20)
        low_buttons.addWidget(quit, alignment=Qt.AlignmentFlag.AlignRight)
        lk.addLayout(low_buttons)

        profile_card.setLayout(lk)

        lk_2.addWidget(profile_card)
        pr.setLayout(lk_2)

        self.profile.addWidget(pr)
        self.info_profile.setLayout(self.profile)

    def load_tariffs(self):
        self.wid = QVBoxLayout()

        self.tar = QWidget()
        self.tar.setStyleSheet("background-color: white;")

        self.tariffs = QVBoxLayout()

        named_widget = QLabel("Тарифы")
        named_widget.setStyleSheet("""
                                    QLabel {
                                        font-size: 25px;
                                    }
        """)
        self.tariffs.addWidget(named_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        heget_tarrifs = QWidget()

        tariff_1 = QHBoxLayout()

        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, Title, Internet, Minutes, Sms, Price FROM Tariffs")

        result = cursor.fetchall()
        cursor.execute("SELECT id, id_tariff, id_user FROM Connected_tariffs WHERE id_user=?", (self.user[0][0],))
        result_2 = cursor.fetchall()
        result = list(filter(lambda x: result_2[0][1] != x[0], result))
        cursor.close()
        connection.close()

        for tar in result:
            l = QWidget()

            l.setFixedWidth(200)
            l.setFixedHeight(250)

            l.setStyleSheet("background-color: #ddffec; border-radius: 20px; font-family: Arial, sans-serif;")

            pl = QVBoxLayout()
            ver_buttons = QHBoxLayout()

            p1 = QLabel(str(tar[1]))
            p1.setStyleSheet("font-size: 18px; font-weight: 500; line-height: 24px;")
            p2 = QLabel("Интернет: " + str(tar[2])+" ГБ")
            p2.setStyleSheet("font size: 15px;")
            p3 = QLabel("Минуты: " + str(tar[3])+" минут")
            p4 = QLabel("Sms: " + str(tar[4]) + " сообщений")
            p5 = QLabel("Цена за 30 дней: " + str(tar[5]) + " ₽")
            p6 = QPushButton("Подключить")
            p6.clicked.connect(partial(self.response_change_tarrif, tar))
            p7 = QPushButton("Подробнее")
            p6.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CAF50;
                                        color: white;
                                        border: none;
                                        padding: 8px 10px;
                                        font-size: 11px;
                                        border-radius: 5px;
                                    }
                                    QPushButton:hover {
                                        background-color: #45a049;
                                    }
                                    QPushButton:pressed {
                                        background-color: #3e8e41;
                                    }
                                """)
            p7.setStyleSheet("""
                                    QPushButton {
                                        background-color: purple;
                                        color: white;
                                        border: none;
                                        padding: 8px 10px;
                                        font-size: 11px;
                                        border-radius: 5px;
                                    }
                                """)

            pl.addStretch()
            pl.addWidget(p1, alignment=Qt.AlignmentFlag.AlignHCenter)
            pl.addStretch()
            pl.addWidget(p2, alignment=Qt.AlignmentFlag.AlignHCenter)
            pl.addWidget(p3, alignment=Qt.AlignmentFlag.AlignHCenter)
            pl.addWidget(p4, alignment=Qt.AlignmentFlag.AlignHCenter)
            pl.addWidget(p5, alignment=Qt.AlignmentFlag.AlignHCenter)
            ver_buttons.addWidget(p6)
            ver_buttons.addWidget(p7)
            pl.addLayout(ver_buttons)
            pl.addStretch()

            l.setLayout(pl)

            tariff_1.addWidget(l)

        button_back = QPushButton("Назад")
        button_back.clicked.connect(self.back_menu_from_tariffs)
        button_back.setFixedWidth(100)
        button_back.setFixedHeight(40)
        button_back.setStyleSheet("background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        heget_tarrifs.setLayout(tariff_1)

        self.tariffs.addWidget(heget_tarrifs)
        self.tariffs.addWidget(button_back, alignment=Qt.AlignmentFlag.AlignRight)

        self.tar.setLayout(self.tariffs)

        self.wid.addWidget(self.tar)

        self.widget_tariffs.setLayout(self.wid)


    def load_service(self):
        self.tabs = QTabWidget()

        widget_calls = QWidget()
        widget_internet = QWidget()

        tab_calls = QVBoxLayout()
        tab_internet = QVBoxLayout()

        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, type_of_service, description, price, type_of_written, text_for_written, value, url_tar FROM Services")
        result = cursor.fetchall()

        cursor.execute("SELECT id_service, id_user FROM Connected_services WHERE id_user=?", (self.user[0][0],))
        con_services = cursor.fetchall()
        for service in con_services:
            result = list(filter(lambda x: x[0] != service[0], result))
        internet_services = list(filter(lambda x: x[2] == "Интернет", result))
        call_services = list(filter(lambda x: x[2] == "Звонки" or x[2] == "Сообщения", result))

        for i in range(0, len(internet_services), 3):
            parts = internet_services[i:i+3]
            parts_layout = QHBoxLayout()
            for part in parts:
                info = QWidget()
                info.setStyleSheet("background-color: #ddffec; border-radius: 20px; font-family: Arial, sans-serif;")
                info.setFixedWidth(300)
                info.setFixedHeight(250)

                info_vbox = QVBoxLayout()
                button_hbox = QHBoxLayout()

                named_service = QLabel(str(part[1]))
                named_service.setStyleSheet("font-size: 18px; font-weight: 500; line-height: 24px;")
                description = QLabel(f"Описание: " + ' '.join(part[3].split('\n')))
                price = QLabel(str(part[6]))
                value_internet = QLabel(str(part[7]))
                url =   QLabel(part[8])
                info_vbox.addWidget(named_service, alignment=Qt.AlignmentFlag.AlignHCenter)
                info_vbox.addWidget(description)
                info_vbox.addWidget(price)
                info_vbox.addWidget(value_internet)

                conn = QPushButton("Подключить")
                conn.clicked.connect(partial(self.connect_service, part))
                details = QPushButton("Подробнее")
                button_hbox.addWidget(conn)
                button_hbox.addWidget(details)

                info_vbox.addLayout(button_hbox)
                info.setLayout(info_vbox)
                parts_layout.addWidget(info)

            tab_internet.addLayout(parts_layout)

        for j in range(0, len(call_services), 4):
            parts = call_services[j:j+4]
            parts_layout = QHBoxLayout()
            for part in parts:
                info = QWidget()
                info.setStyleSheet("background-color: #ddffec; border-radius: 20px; font-family: Arial, sans-serif;")
                info.setFixedWidth(300)
                info.setFixedHeight(250)

                info_vbox = QVBoxLayout()
                button_hbox = QHBoxLayout()

                named_service = QLabel(str(part[1]))
                named_service.setStyleSheet("font-size: 18px; font-weight: 500; line-height: 24px;")
                description = QLabel("Описание: " + str(part[3]))
                price = QLabel(str(part[6]))
                value_internet = QLabel(str(part[7]))
                url = QLabel(part[8])
                info_vbox.addWidget(named_service, alignment=Qt.AlignmentFlag.AlignHCenter)
                info_vbox.addWidget(description)
                info_vbox.addWidget(price)
                info_vbox.addWidget(value_internet)

                conn = QPushButton("Подключить")
                conn.clicked.connect(partial(self.connect_service, part))
                details = QPushButton("Подробнее")
                button_hbox.addWidget(conn)
                button_hbox.addWidget(details)

                info_vbox.addLayout(button_hbox)
                info.setLayout(info_vbox)
                parts_layout.addWidget(info)
            tab_calls.addLayout(parts_layout)

        button_back_calls = QPushButton("Назад")
        button_back_calls.setFixedWidth(100)
        button_back_calls.setFixedHeight(40)
        button_back_calls.setStyleSheet(
            "background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")

        button_back_calls.clicked.connect(self.back_menu_from_services)
        button_back_internet = QPushButton("Назад")
        button_back_internet.setFixedWidth(100)
        button_back_internet.setFixedHeight(40)
        button_back_internet.setStyleSheet(
            "background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")
        button_back_internet.clicked.connect(self.back_menu_from_services)

        tab_calls.addWidget(button_back_calls, alignment = Qt.AlignmentFlag.AlignRight)
        tab_internet.addWidget(button_back_internet, alignment=Qt.AlignmentFlag.AlignRight)

        widget_internet.setLayout(tab_internet)
        widget_calls.setLayout(tab_calls)

        self.tabs.addTab(widget_internet, "Интернет")
        self.tabs.addTab(widget_calls, "Звонки и сообщения")

        self.tabs_widget = QVBoxLayout()
        self.tabs_widget.addWidget(self.tabs)

        self.widget_services.setLayout(self.tabs_widget)

    def response_change_tarrif(self, tariff):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        if self.user[0][7] - tariff[5] > 0:
            cursor.execute("UPDATE Connected_tariffs SET id_tariff=?, date_connected=?, remainder_internet=?, remainder_sms=?, remainder_minutes=? WHERE id_user=?", (tariff[0], date.today().strftime("%d.%m.%Y"), tariff[2], tariff[4], tariff[3], self.user[0][0]))
            connection.commit()
            print("новый тариф подключен")
            cursor.execute("UPDATE Users SET balance=? WHERE id=?", (self.user[0][7]-tariff[5], self.user[0][0]))
            connection.commit()
            print("1")
            id = self.user[0][0]
            self.user = cursor.execute("SELECT * FROM Users WHERE id=?", (id,)).fetchall()
            print(self.user)
            self.back_menu_from_con_tar()
        else:
            print("Ошибка")
        cursor.close()
        connection.close()


    def connect_service(self, service):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        print(service)
        print(self.user)
        cursor.execute("INSERT INTO Connected_services (id_service, id_user, date_connected, date_written_off, payment_status, remainder) VALUES (?, ?, ?, ?, ?, ?)", (int(service[0]), self.user[0][0], date.today().strftime("%d.%m.%Y"), (date.today()+timedelta(days=30)).strftime("%d.%m.%Y"), "Не оплачено", service[7]))
        print("1")
        connection.commit()
        cursor.close()
        connection.close()
        self.back_menu_turn_service()




    def rephil_balance(self):
        layout_balance = QVBoxLayout()

        print(self.user)

        named = QLabel(f"Ваш баланс: {self.user[0][7]} ₽")
        named.setFont(QFont("Arial", 18))

        button_exit = QPushButton("Назад")
        button_exit.clicked.connect(self.back_menu_from_balance)
        button_exit.setStyleSheet(
            "background-color: lightblue; border-radius: 5px; font-family: Arial, sans-serif; padding: 8px 10px; font-size: 14px;")

        frame_balance = QFrame()
        v_frame = QVBoxLayout()
        frame_balance.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 10px;")

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Введите сумму от 10 до 10000 ₽")
        self.amount.setStyleSheet("""
                                            QLineEdit {
                                                border: 0.5px solid black;
                                                border-radius: 5px;
                                            }
                                """)
        self.amount.setFixedWidth(250)
        self.amount.setFixedWidth(300)

        self.button_amount = QPushButton("Пополнить")
        self.button_amount.clicked.connect(self.update_balance)
        self.button_amount.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CAF50;
                                        color: white;
                                        border: none;
                                        padding: 10px 20px;
                                        font-size: 16px;
                                        border-radius: 15px;
                                    }
                                    QPushButton:hover {
                                        background-color: #45a049;
                                    }
                                    QPushButton:pressed {
                                        background-color: #3e8e41;
                                    }
                                """)

        frame_balance.setFixedWidth(400)
        frame_balance.setFixedHeight(400)

        layout_balance.addWidget(named, alignment = Qt.AlignmentFlag.AlignHCenter)
        v_frame.addWidget(self.amount, alignment = Qt.AlignmentFlag.AlignHCenter)
        v_frame.addWidget(self.button_amount, alignment = Qt.AlignmentFlag.AlignHCenter)
        frame_balance.setLayout(v_frame)
        layout_balance.addStretch()
        layout_balance.addWidget(frame_balance, alignment = Qt.AlignmentFlag.AlignHCenter)
        layout_balance.addStretch()
        layout_balance.addWidget(button_exit, alignment = Qt.AlignmentFlag.AlignRight)


        self.widget_balance.setLayout(layout_balance)

    def turn_off_service(self, service):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Connected_services WHERE id_service=? AND id_user=?", (service[0], self.user[0][0]))
        connection.commit()
        cursor.close()
        connection.close()
        self.back_menu_from_off_service()

    def update_balance(self):
        bal = self.amount.text()
        try:
            if 10 <= int(bal) <= 10000:
                connection = sqlite3.connect("Users.db")
                cursor = connection.cursor()
                cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (float(bal) + self.user[0][7], self.user[0][0]))
                connection.commit()
                us = self.user[0][0]
                print(us)
                cursor.execute("SELECT * FROM Users WHERE id=?", (us,))
                self.user = cursor.fetchall()
                print(self.user)
                cursor.close()
                connection.close()
                self.back_menu_from_balance()
            else:
                QMessageBox.warning(self, "Ошибка", "Введена либо слишком маленькая сумма, либо слишком большая")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введен неверный тип данных")

    def show_tariffs(self):
        self.widget_menu.hide()
        self.main_layout.addWidget(self.widget_tariffs)
        self.widget_tariffs.show()

    def show_service(self):
        self.widget_menu.hide()
        self.main_layout.addWidget(self.widget_services)
        self.widget_services.show()

    def show_profile(self):
        self.widget_menu.hide()
        self.main_layout.addWidget(self.info_profile)
        self.info_profile.show()

    def show_my_tariff(self):
        self.widget_menu.hide()
        self.main_layout.addWidget(self.widget_my_tariff)
        self.widget_my_tariff.show()

    def show_change(self):
        self.widget_my_tariff.hide()
        self.main_layout.addWidget(self.widget_tariffs)
        self.widget_tariffs.show()

    def show_my_service(self):
        self.widget_menu.hide()
        self.main_layout.addWidget(self.widget_my_service)
        self.widget_my_service.show()

    def show_bal_am(self):
        self.back_menu_from_balance()
        self.widget_menu.hide()
        self.main_layout.addWidget(self.widget_balance)
        self.widget_balance.show()

    def quit_lk(self):
        self.create_layout()
        self.widget_login = QWidget()
        self.setup_login()

        self.widget_tariffs = QWidget()

        self.widget_services = QWidget()

        self.widget_menu = QWidget()

        self.info_profile = QWidget()

        self.widget_my_tariff = QWidget()
        self.info_profile = QWidget()

        self.widget_my_service = QWidget()

        self.widget_balance = QWidget()

        self.main_layout.addWidget(self.widget_login)

    def back_menu_from_tariffs(self):
        self.widget_tariffs.hide()
        self.main_menu_user()
        self.widget_menu.show()

    def back_menu_from_services(self):
        self.widget_services.hide()
        self.main_menu_user()
        self.widget_menu.show()

    def back_menu_from_profile(self):
        self.info_profile.hide()
        self.main_menu_user()
        self.widget_menu.show()

    def back_menu_from_my_tariff(self):
        self.widget_my_tariff.hide()
        self.main_menu_user()
        self.widget_menu.show()

    def back_menu_from_my_services(self):
        self.widget_my_service.hide()
        self.main_menu_user()
        self.widget_menu.show()

    def back_menu_from_balance(self):
        self.widget_balance.hide()
        self.main_menu_user()
        self.widget_menu.show()
        self.amount = QLineEdit()
        if self.widget_balance:
            self.widget_balance.deleteLater()
        self.widget_balance = QWidget()
        self.rephil_balance()

    def back_menu_from_con_tar(self):
        self.widget_tariffs.hide()
        self.widget_menu.hide()
        if self.widget_menu:
            self.widget_menu.deleteLater()
        if self.widget_tariffs:
            self.widget_tariffs.deleteLater()
        if self.widget_my_tariff:
            self.widget_my_tariff.deleteLater()
        self.widget_menu = QWidget()
        self.main_menu_user()
        self.main_layout.addWidget(self.widget_menu)
        self.widget_tariffs = QWidget()
        self.load_tariffs()
        self.main_layout.addWidget(self.widget_tariffs)
        self.widget_tariffs.hide()
        self.widget_my_tariff = QWidget()
        self.my_tariff()
        self.main_layout.addWidget(self.widget_my_tariff)
        self.widget_my_tariff.hide()
        self.widget_menu.show()
    def back_menu_from_off_service(self):
        self.widget_menu.hide()
        self.widget_my_service.hide()
        if self.widget_menu:
            self.widget_menu.deleteLater()
        if self.widget_my_service:
            self.widget_my_service.deleteLater()
        self.widget_menu = QWidget()
        self.main_menu_user()
        self.main_layout.addWidget(self.widget_menu)
        self.widget_menu.show()
        self.widget_my_service = QWidget()
        self.my_services()
        self.main_layout.addWidget(self.widget_my_service)
        self.widget_my_service.hide()

    def back_menu_turn_service(self):
        self.widget_services.hide()
        self.widget_my_service.hide()
        self.widget_menu.hide()
        if self.widget_menu:
            self.widget_menu.deleteLater()
        self.widget_menu = QWidget()
        self.main_menu_user()
        self.main_layout.addWidget(self.widget_menu)
        self.widget_menu.show()
        if self.widget_services:
            self.widget_services.deleteLater()
        self.widget_services = QWidget()
        self.load_service()
        self.main_layout.addWidget(self.widget_services)
        self.widget_services.hide()
        if self.widget_my_service:
            self.widget_my_service.deleteLater()
        self.widget_my_service = QWidget()
        self.my_services()
        self.main_layout.addWidget(self.widget_my_service)
        self.widget_my_service.hide()

    def create_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())