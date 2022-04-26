#GUI форма регистрации в качестве интерфейса использована библиотека PyQT5, в качестве базы данных использована MongoDB
import sys
import pymongo
from PyQt5 import QtCore, QtGui, QtWidgets
from des import *


class Gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.centerOnScreen()

        self.authorization_status = False
        #Вставить ссылку от собственного mondodb
        self.client = pymongo.MongoClient("YOUR DATABASE LINK!!!")
        self.ui.pushButton.clicked.connect(self.register)
        self.ui.pushButton_2.clicked.connect(self.login)

    # Функция выравнивания окна по центру
    def centerOnScreen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move(int(resolution.width() / 2) - int(self.frameSize().width() / 2),
                  int(resolution.height() / 2) - int(self.frameSize().height() / 2))

    def check_data(self):
        login = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()

        # Ищем логин в базе данных
        if login and passw:
            search_login = self.client.testdb.users.find_one({"nickname": login})
            # Eсли значение найдено
            if search_login:
                return "value_exists"
            # Если значение не найдено
            else:
                return "value_not_found"
        # Если данные не заполнены
        else:
            return "no_data_available"

    def login(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                # Ищем запись и проверяем правильность пароля
                login = self.ui.lineEdit.text()
                passw = self.ui.lineEdit_2.text()
                user_document = self.client.testdb.users.find_one({"nickname": login})

                if user_document and passw == user_document["password"]:
                    message = "Успешная авторизация!"
                    QtWidgets.QMessageBox.about(self, "Уведомление", message)
                    self.authorization_status = True
                else:
                    message = "Данные введены не корректно"
                    QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                message = "Такой пользователь не зарегистрирован!"
                QtWidgets.QMessageBox.about(self, "Уведомление", message)
            elif result == "no_data_available":
                message = "Необходимо ввести данные!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

        else:
            message = "Такой пользователь зарегистрирован!"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)

    def register(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                message = "Такой логин уже используется"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                data = {
                    "nickname": self.ui.lineEdit.text(),
                    # Я знаю, что пароли не хешированы =)
                    "password": self.ui.lineEdit_2.text()
                }
                self.client.testdb.users.insert_one(data)
                message = "Регистрация прошла успешно!"
                QtWidgets.QMessageBox.about(self, "Уведомление", message)
                self.authorization_status = True

            elif result == "no_data_available":
                message = "Необходимо ввести данные"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)
        else:
            message = "Вы уже авторизированы!"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec_())
