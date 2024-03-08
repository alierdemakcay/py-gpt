from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QTextCursor
import sys
import webbrowser
komutlar = {
    "hello" : "hello !",
    "hi" : " hi",
    "gpt" : "I ....Gpt",
}

class TypingEffect(QObject):
    typingFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.type_next_word)
        self.words = []
        self.current_word_index = 0

    def start_typing(self, text, interval):
        self.text = text
        self.words = text.split()
        self.current_word_index = 0
        self.timer.start(interval)

    def type_next_word(self):
        if self.current_word_index < len(self.words):
            self.parent().append_text(self.words[self.current_word_index] + " ")
            self.current_word_index += 1
        else:
            self.typingFinished.emit()
            self.timer.stop()

class GPTArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GPT') #Isim buraya gelecek . Name goes here
        self.setFixedSize(1000, 800)  

        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: #333333; color: #00ccff; border-radius: 10px;")
        
        self.label = QLabel("GPT")
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)  
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: #191919; color: #00ccff; border-radius: 10px;")
        font = QFont("Arial", 12)  
        self.text_edit.setFont(font)
        self.layout.addWidget(self.text_edit)

        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("background-color: #191919; color: #00ccff; border-radius: 10px;")
        font = QFont("Arial", 12)  
        self.input_line.setFont(font)
        self.layout.addWidget(self.input_line)

        self.search_button = QPushButton('↲')
        self.search_button.setStyleSheet("background-color: #008CBA; color: #ffffff; border-radius: 10px; center ; ")
        font = QFont("Arial", 20)  
        self.search_button.setFont(font)
        self.search_button.clicked.connect(self.arama_yap)
        self.search_button.setFixedSize(150, 50) 
        self.layout.addWidget(self.search_button)

        self.setLayout(self.layout)

        self.input_line.returnPressed.connect(self.arama_yap)

        self.typing_effect = TypingEffect(self)
        self.typing_effect.typingFinished.connect(self.typing_finished)

    def komut_calistir(self, kullanici_girdisi):
        kullanici_girdisi = kullanici_girdisi.lower()
        for komut, yanit in komutlar.items():
            if komut in kullanici_girdisi:
                return yanit
        
        query = kullanici_girdisi
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        
        return "Sorry, I couldn't find any information about what you asked about. But I searched the Internet, maybe this will help you."

    def arama_yap(self):
        kullanici_girdisi = self.input_line.text()
        cevap = self.komut_calistir(kullanici_girdisi)
        
        self.text_edit.setTextColor(QColor('#00ccff'))
        self.text_edit.append('\nSEN : ' + kullanici_girdisi)
        self.text_edit.append('GPT : ')
        self.typing_effect.start_typing(cevap, 200)

    def append_text(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)

    def typing_finished(self):
        self.input_line.clear()
        self.text_edit.moveCursor(QTextCursor.End)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    arayuz = GPTArayuz()
    arayuz.show()
    sys.exit(app.exec_())