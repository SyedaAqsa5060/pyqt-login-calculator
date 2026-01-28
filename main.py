import sys
import pyodbc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


# ---------- Database Connection ----------
def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'       # 👈 apna SQL Server name check kar lo (SSMS se)
            'DATABASE=hicup;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        QMessageBox.critical(None, "Database Error", str(e))
        return None


# ---------- Base Styling Function ----------
def set_dark_neon_theme(widget):
    widget.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            font-family: 'Segoe UI';
        }
        QLabel {
            color: #e0e7ff;
            font-size: 16px;
            font-weight: 600;
        }
        QLineEdit {
            background-color: #020617;
            color: #e0e7ff;
            border: 2px solid #38bdf8;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #22d3ee;
        }
        QPushButton {
            background-color: #38bdf8;
            color: #020617;
            border-radius: 12px;
            padding: 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #22d3ee;
        }
    """)



# ---------- Signup Window ----------
class SignupUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Made by Aqsa")
        self.setGeometry(520, 260, 400, 360)
        set_dark_neon_theme(self)

        layout = QVBoxLayout()
        title = QLabel("Create Your Account 💫")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        self.fname = QLineEdit()
        self.fname.setPlaceholderText("First Name")
        layout.addWidget(self.fname)

        self.lname = QLineEdit()
        self.lname.setPlaceholderText("Last Name")
        layout.addWidget(self.lname)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.signup_btn = QPushButton("Sign Up")
        layout.addWidget(self.signup_btn)
        self.signup_btn.clicked.connect(self.signup_user)

        self.login_btn = QPushButton("Already have an account? Login")
        layout.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.go_to_login)

        self.setLayout(layout)

    def signup_user(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO signup (First_name, Last_name, Email, Password)
                    VALUES (?, ?, ?, ?)
                """, (self.fname.text(), self.lname.text(), self.email.text(), self.password.text()))
                conn.commit()
                QMessageBox.information(self, "Success", "🎉 Signup Successful!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    def go_to_login(self):
        self.login_window = LoginUI()
        self.login_window.show()
        self.close()


# ---------- Login Window ----------
class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Made by Aqsa" )
        self.setGeometry(520, 260, 400, 300)
        set_dark_neon_theme(self)

        layout = QVBoxLayout()
        title = QLabel("Welcome Back 💜")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = QPushButton("Login")
        layout.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.login_user)

        self.signup_btn = QPushButton("Create New Account")
        layout.addWidget(self.signup_btn)
        self.signup_btn.clicked.connect(self.go_to_signup)

        self.setLayout(layout)

    def login_user(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM signup WHERE Email=? AND Password=?", 
                               (self.email.text(), self.password.text()))
                user = cursor.fetchone()
                if user:
                    QMessageBox.information(self, "Success", "🎉 Login Successful!")
                    self.open_calculator()
                else:
                    QMessageBox.warning(self, "Failed", "❌ Invalid Email or Password!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    def open_calculator(self):
        self.calc_window = CalculatorUI()
        self.calc_window.show()
        self.close()

    def go_to_signup(self):
        self.signup_window = SignupUI()
        self.signup_window.show()
        self.close()


# ---------- Calculator Window ----------
from PyQt5.QtWidgets import QMainWindow
from cal import Ui_MainWindow   # 👈 cal.py ka correct name

class CalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # OPTIONAL: window title
        self.setWindowTitle("Calculator - Made by Aqsa")
         # display reference
        self.display = self.ui.label

        # number buttons
        self.ui.push_0 = self.ui.pushButton_19
        self.ui.push_1.clicked.connect(lambda: self.add_text("1"))
        self.ui.push_2.clicked.connect(lambda: self.add_text("2"))
        self.ui.push_3.clicked.connect(lambda: self.add_text("3"))
        self.ui.push_4.clicked.connect(lambda: self.add_text("4"))
        self.ui.push_5.clicked.connect(lambda: self.add_text("5"))
        self.ui.push_6.clicked.connect(lambda: self.add_text("6"))
        self.ui.push_7.clicked.connect(lambda: self.add_text("7"))
        self.ui.push_8.clicked.connect(lambda: self.add_text("8"))
        self.ui.push_9.clicked.connect(lambda: self.add_text("9"))
        self.ui.push_0.clicked.connect(lambda: self.add_text("0"))

        # operators
        self.ui.pushButton_10.clicked.connect(lambda: self.add_text("+"))
        self.ui.push_minus.clicked.connect(lambda: self.add_text("-"))
        self.ui.psuh_multi.clicked.connect(lambda: self.add_text("*"))
        self.ui.push_div.clicked.connect(lambda: self.add_text("/"))
        self.ui.push_dot.clicked.connect(lambda: self.add_text("."))

        # actions
        self.ui.push_clear.clicked.connect(self.clear_display)
        self.ui.push_del.clicked.connect(self.delete_last)
        self.ui.push_equal.clicked.connect(self.calculate)
    def add_text(self, value):
        if self.display.text() == "0":
            self.display.setText(value)
        else:
            self.display.setText(self.display.text() + value)

    def clear_display(self):
        self.display.setText("0")

    def delete_last(self):
        text = self.display.text()
        self.display.setText(text[:-1] if len(text) > 1 else "0")

    def calculate(self):
        try:
            result = str(eval(self.display.text()))
            self.display.setText(result)
        except:
            self.display.setText("Error")



# ---------- Main ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUI()
    window.show()
    sys.exit(app.exec_())
