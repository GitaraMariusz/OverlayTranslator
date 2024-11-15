import json
from PyQt5 import QtWidgets, QtCore
from googletrans import Translator
import sys
import keyboard
import os

translator = Translator()

languages = ["en", "ja", "es", "fr", "de"]
config_file = "config.json"  

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.last_input_text = ""
        self.shortcut = "ctrl+alt+t"
        self.source_lang = "en"  
        self.target_lang = "ja"  
        self.settings_window = None
        self.settings_was_open = False

        self.load_settings()  

        self.init_ui()
        self.update_shortcut(self.shortcut)

    def load_settings(self):
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as file:
                    config = json.load(file)
                    self.shortcut = config.get("shortcut", self.shortcut)
                    self.source_lang = config.get("source_lang", self.source_lang)
            except json.JSONDecodeError:
                self.shortcut = "ctrl+alt+t"
                self.source_lang = "en"
                self.save_settings() 
        else:
            self.shortcut = "ctrl+alt+t"
            self.source_lang = "en"

    def save_settings(self):
        config = {
            "shortcut": self.shortcut,
            "source_lang": self.source_lang
        }
        with open(config_file, "w") as file:
            json.dump(config, file)

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)

        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        width = int(screen_width * 0.18)       
        height = int(screen_height * 0.2)     
        x_position = int(screen_width * 0.03) 
        y_position = int(screen_height * 0.75)  

        self.setGeometry(x_position, y_position, width, height)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.input_box = QtWidgets.QTextEdit(self)
        self.input_box.setPlaceholderText("Type text here...")
        self.input_box.textChanged.connect(self.on_input_change)
        layout.addWidget(self.input_box)

        self.output_box = QtWidgets.QTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Translation will appear here")
        layout.addWidget(self.output_box)

        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setContentsMargins(0, 5, 0, 5)

        self.target_lang_combo = QtWidgets.QComboBox(self)
        self.target_lang_combo.addItems([lang for lang in languages])  
        self.target_lang_combo.setCurrentText(self.target_lang) 
        self.target_lang_combo.currentIndexChanged.connect(self.on_target_language_change)
        bottom_layout.addWidget(self.target_lang_combo)

        self.settings_button = QtWidgets.QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings)
        bottom_layout.addWidget(self.settings_button)

        layout.addLayout(bottom_layout)

        self.debounce_timer = QtCore.QTimer()
        self.debounce_timer.setInterval(500)  
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.perform_translation)

    def update_shortcut(self, new_shortcut):
        try:
            keyboard.remove_hotkey(self.shortcut)
        except KeyError:
            pass

        self.shortcut = new_shortcut
        keyboard.add_hotkey(self.shortcut, self.toggle_visibility)

    def toggle_visibility(self):
        if self.isHidden():
            self.show()
            if self.settings_was_open and self.settings_window:
                self.settings_window.show()
        else:
            self.hide()
            if self.settings_window and self.settings_window.isVisible():
                self.settings_was_open = True
                self.settings_window.hide()
            else:
                self.settings_was_open = False

    def on_input_change(self):
        self.debounce_timer.start()

    def on_target_language_change(self):
        self.target_lang = self.target_lang_combo.currentText() 
        input_text = self.input_box.toPlainText().strip()
        
        if input_text:
            self.translate_text()

    def perform_translation(self):
        input_text = self.input_box.toPlainText().strip()

        if input_text != self.last_input_text:
            self.last_input_text = input_text
            if input_text:
                self.translate_text()
            else:
                self.output_box.setPlainText("Translation will appear here")

    def translate_text(self):
        text = self.input_box.toPlainText().strip()
        if text:
            result = translator.translate(text, src=self.source_lang, dest=self.target_lang)
            self.output_box.setPlainText(result.text)

    def open_settings(self):
        if self.settings_window is not None and self.settings_window.isVisible():
            self.settings_window.close()
            self.settings_was_open = False
        else:
            self.settings_window = SettingsWindow(self)
            self.settings_window.setGeometry(self.x(), self.y() - self.settings_window.height(), self.width(), int(self.height() * 0.8))
            self.settings_window.show()
            self.settings_was_open = True

class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)

        self.setFixedSize(self.main_window.width(), int(self.main_window.height() * 0.8))
        self.setStyleSheet("""
            background-color: #FFFFFF;
            color: #000000;
            font-family: Arial, sans-serif;
        """)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        self.setLayout(layout)

        shortcut_label = QtWidgets.QLabel("Shortcut:", self)
        layout.addWidget(shortcut_label)
        
        self.shortcut_entry = QtWidgets.QLineEdit(self)
        self.shortcut_entry.setText(self.main_window.shortcut)
        layout.addWidget(self.shortcut_entry)

        source_lang_label = QtWidgets.QLabel("Source Language:", self)
        layout.addWidget(source_lang_label)

        self.source_lang_combo = QtWidgets.QComboBox(self)
        self.source_lang_combo.addItems(languages)
        self.source_lang_combo.setCurrentText(self.main_window.source_lang)
        layout.addWidget(self.source_lang_combo)

        save_button = QtWidgets.QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button, alignment=QtCore.Qt.AlignCenter)

    def save_settings(self):
        new_shortcut = self.shortcut_entry.text().strip()
        self.main_window.source_lang = self.source_lang_combo.currentText()

        if new_shortcut:
            self.main_window.update_shortcut(new_shortcut)
        
        self.main_window.save_settings()
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
