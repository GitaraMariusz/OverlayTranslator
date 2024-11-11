from PyQt5 import QtWidgets, QtCore
from googletrans import Translator
import sys
import keyboard

translator = Translator()

last_input_text = ""
shortcut = "ctrl+alt+t"
source_lang = "en"
languages = ["en", "ja", "es", "fr", "de", "zh"]

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)

        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(50, screen.height() - 300, 300, 150)  

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.input_box = QtWidgets.QTextEdit(self)
        self.input_box.setPlaceholderText("Type text here...")
        self.input_box.textChanged.connect(self.on_input_change)
        layout.addWidget(self.input_box)

        self.debounce_timer = QtCore.QTimer()
        self.debounce_timer.setInterval(500)  
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.perform_translation)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.target_lang_combo = QtWidgets.QComboBox(self)
        self.target_lang_combo.addItems([lang for lang in languages])  
        bottom_layout.addWidget(self.target_lang_combo)

        self.settings_button = QtWidgets.QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings)
        bottom_layout.addWidget(self.settings_button)

        layout.addLayout(bottom_layout)

        self.popup_window = PopupWindow()
        
        self.update_shortcut(shortcut)

    def update_shortcut(self, new_shortcut):
        global shortcut
        try:
            keyboard.remove_hotkey(shortcut)
        except KeyError:
            pass
    
        shortcut = new_shortcut
        keyboard.add_hotkey(shortcut, self.toggle_visibility)

    def toggle_visibility(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def on_input_change(self):
        self.debounce_timer.start()  

    def perform_translation(self):
        global last_input_text
        input_text = self.input_box.toPlainText().strip()

        if input_text != last_input_text and input_text:
            last_input_text = input_text
            self.translate_text(input_text)
        elif not input_text:
            self.popup_window.hide()
            last_input_text = ""

    def translate_text(self, text):
        global source_lang
        target_lang = self.target_lang_combo.currentText()
        result = translator.translate(text, src=source_lang, dest=target_lang)
        self.popup_window.show_translation(result.text, self)

    def open_settings(self):
        if hasattr(self, 'settings_window') and self.settings_window.isVisible():
            self.settings_window.close() 
        else:
            self.settings_window = SettingsWindow(self)
            self.settings_window.show()


class PopupWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)
        self.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.text_display = QtWidgets.QTextEdit(self)
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

    def show_translation(self, text, parent):
        self.text_display.setPlainText(text)
        self.move(parent.x(), parent.y() + parent.height() + 10)
        self.show()


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)
        self.setFixedSize(300, 150)
        
        self.setStyleSheet("background-color: white; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        shortcut_layout = QtWidgets.QHBoxLayout()
        shortcut_label = QtWidgets.QLabel("Open Shortcut:", self)
        shortcut_layout.addWidget(shortcut_label)

        self.shortcut_entry = QtWidgets.QLineEdit(self)
        self.shortcut_entry.setText(shortcut)
        shortcut_layout.addWidget(self.shortcut_entry)
        layout.addLayout(shortcut_layout)

        language_layout = QtWidgets.QHBoxLayout()
        lang_label = QtWidgets.QLabel("Source Language:", self)
        language_layout.addWidget(lang_label)

        self.source_lang_combo = QtWidgets.QComboBox(self)
        self.source_lang_combo.addItems(languages)
        self.source_lang_combo.setCurrentText(source_lang)
        language_layout.addWidget(self.source_lang_combo)
        layout.addLayout(language_layout)

        save_button = QtWidgets.QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button, alignment=QtCore.Qt.AlignCenter)

    def save_settings(self):
        global source_lang
        new_shortcut = self.shortcut_entry.text().strip()
        source_lang = self.source_lang_combo.currentText()

        if new_shortcut:
            self.main_window.update_shortcut(new_shortcut)
        
        self.close()

    def show(self):
        extra_offset = 20  
        if self.main_window.popup_window.isVisible():
            self.move(self.main_window.popup_window.x(), self.main_window.popup_window.y() - self.height() + extra_offset)
        else:
            self.move(self.main_window.x(), self.main_window.y() - self.height() + extra_offset)
        super().show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
