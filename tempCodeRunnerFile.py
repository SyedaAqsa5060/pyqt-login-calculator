import sys
import hashlib
import pyodbc
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


# ---------- DATABASE CONNECTION ----------
def connect_db():
    """Connect to SQL Server database"""
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'           # ⚙️ Change if your SQL Server name is different
            'DATABASE=hicup;'             # ❌ No spaces before/after '=' or ';'
            'Trusted_Connection=yes;'
        )
        return connection
    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"❌ Connection failed: {str(e)}")
        return None


# ---------- SIGNUP WINDOW ----------
class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self, main_app, ui_class):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.main_app = main_app

        # Button connections
        self.ui.pushButton_3.clicked.connect(self.signup_user)
        self.ui.pushButton_2.clicked.connect(self.goto_login)

    def signup_user(self):
        """Handle user signup"""
        try:
            first_name = self.ui.lineEdit_first.text().strip()
            last_name = self.ui.lineEdit_last.text().strip()
            email = self.ui.lineEdit_email.text().strip()
            password = self.ui.lineEdit_password.text().strip()
        except AttributeError:
            QMessageBox.critical(self, "Error", "⚠️ Check lineEdit names in sign_Up.ui file")
            return

        if not all([first_name, last_name, email, password]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = connect_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO signup (First_name, Last_name, Email, Password)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, email, password_hash))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "🎉 Account created successfully!")
            self.goto_login()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def goto_login(self):
        self.main_app.open_login()


# ---------- LOGIN WINDOW ----------
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, main_app, ui_class):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.main_app = main_app

        # Button connections
        self.ui.pushButton_3.clicked.connect(self.check_login)
        self.ui.pushButton_2.clicked.connect(self.goto_signup)

    def check_login(self):
        """Verify user credentials"""
        try:
            username = self.ui.lineEdit.text().strip()
            password = self.ui.lineEdit_4.text().strip()
        except AttributeError:
            QMessageBox.critical(self, "Error", "⚠️ Check lineEdit names in login.ui file")
            return

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = connect_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM signup WHERE Email=? AND Password=?", (username, password_hash))
            user = cursor.fetchone()
            conn.close()

            if user:
                QMessageBox.information(self, "Welcome", f"Hello {user[1]} 🎉 You’re logged in!")
                self.main_app.open_calculator()
            else:
                QMessageBox.warning(self, "Error", "Invalid Username or Password.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def goto_signup(self):
        self.main_app.open_signup()


# ---------- CALCULATOR WINDOW ----------
class CalculatorWindow(QtWidgets.QMainWindow):
    def __init__(self, main_app, ui_class):
        super().__init__()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.main_app = main_app

        button_map = {
            "pushButton_0": "0", "pushButton_1": "1", "pushButton_2": "2",
            "pushButton_3": "3", "pushButton_4": "4", "pushButton_5": "5",
            "pushButton_6": "6", "pushButton_7": "7", "pushButton_8": "8",
            "pushButton_9": "9", "pushButton_plus": "+", "pushButton_minus": "-",
            "pushButton_mul": "*", "pushButton_div": "/", "pushButton_clear": "C",
            "pushButton_equal": "="
        }

        for name, value in button_map.items():
            if hasattr(self.ui, name):
                button = getattr(self.ui, name)
                if value == "C":
                    button.clicked.connect(self.clear_text)
                elif value == "=":
                    button.clicked.connect(self.calculate_result)
                else:
                    button.clicked.connect(lambda _, v=value: self.add_text(v))

    def add_text(self, text):
        current = self.ui.lineEdit_display.text()
        self.ui.lineEdit_display.setText(current + text)

    def clear_text(self):
        self.ui.lineEdit_display.clear()

    def calculate_result(self):
        try:
            result = str(eval(self.ui.lineEdit_display.text()))
            self.ui.lineEdit_display.setText(result)
        except Exception:
            self.ui.lineEdit_display.setText("Error")


# ---------- MAIN CONTROLLER ----------
class MainApp:
    def __init__(self):
        from sign_Up import Ui_MainWindow as SignupUI
        from login import Ui_MainWindow as LoginUI
        from cal import Ui_MainWindow as CalculatorUI

        self.app = QtWidgets.QApplication(sys.argv)
        self.login_window = LoginWindow(self, LoginUI)
        self.signup_window = SignupWindow(self, SignupUI)
        self.calculator_window = CalculatorWindow(self, CalculatorUI)

    def open_signup(self):
        self.signup_window.show()
        self.login_window.close()
        self.calculator_window.close()

    def open_login(self):
        self.login_window.show()
        self.signup_window.close()
        self.calculator_window.close()

    def open_calculator(self):
        self.calculator_window.show()
        self.signup_window.close()
        self.login_window.close()

    def run(self):
        self.open_login()
        sys.exit(self.app.exec_())


# ---------- RUN APP ----------
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
