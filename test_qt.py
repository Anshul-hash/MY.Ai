from PySide6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)

label = QLabel("Hello ZENA")
label.resize(300, 100)
label.show()

sys.exit(app.exec())
