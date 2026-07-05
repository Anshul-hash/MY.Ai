import sys
from PySide6.QtWidgets import QApplication

from localai_studio.ui.main_window import MainWindow

app = QApplication(sys.argv)

print("Creating window...")
window = MainWindow()
print("Window created.")

window.show()
print("Window shown.")

sys.exit(app.exec())
