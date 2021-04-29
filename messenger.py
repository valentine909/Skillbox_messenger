from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host='http://127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.send_message)
        self.host = host

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def get_messages(self):
        try:
            response = requests.get(self.host + '/messages',
                                    params={'after': self.after}
                                    )
        except:
            return
        messages = response.json()['messages']
        if len(messages) > 0:
            self.show_messages(messages)
            self.after = messages[-1]['time']

    def show_messages(self, messages):
        for message in messages:
            t = datetime.fromtimestamp(int(message['time']))
            self.textBrowser.append(message['name'] + ' ' + str(t))
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        self.textEdit.clear()
        try:
            response = requests.post(self.host + '/send',
                                     json={'name': name,
                                           'text': text}
                                     )
        except:
            self.textBrowser.append('Сервер временно недоступен. Повторите позже')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Сообщение не отправлено')
            self.textBrowser.append('Проверьте имя и текст')
            self.textBrowser.append('')


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()
