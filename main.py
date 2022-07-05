import os
import sys
import webbrowser

import alsaaudio
import speech_recognition
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Voice assistant")
        self.setGeometry(800, 500, 400, 300)

        self.hello_text = QtWidgets.QLabel(self)
        self.hello_text.setText("Здравствуйте! Вас приветствует голосовой ассистент")
        self.hello_text.move(10, 20)
        self.hello_text.adjustSize()

        self.base_text = QtWidgets.QLabel(self)
        self.base_text.move(10, 50)
        self.base_text.adjustSize()

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setText('Push')
        self.run_button.move(10, 100)
        self.run_button.adjustSize()

        self.run_button.clicked.connect(self.add_functions)

    def add_functions(self):
        sr = speech_recognition.Recognizer()
        sr.pause_threshold = 0.5  # изменяем паузу между словами с секунды, до пол секунды
        query = ""

        try:

            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)  # метод предназначение для колибровки шума
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                your_command = "Ваша команда: " + query
                print(your_command)

        except speech_recognition.UnknownValueError:
            self.base_text.setText("Команда не распознана")
            self.base_text.adjustSize()
            print("Сработало исключение ")

        if (query.find("открой диспетчер задач") >= 0) or (query.find("открыть диспетчер задач") >= 0):
            self.base_text.setText('Диспетчер задач открыт')
            self.base_text.adjustSize()
            self.open_task_manager()

        elif (query.find("открой настройки") >= 0) or (query.find("открой настройки системы") >= 0) or \
                (query.find("открыть настройки") >= 0) or (query.find("открыть настройки системы") >= 0):
            self.open_settings()

        elif (query.find("поиск в интернете") >= 0) or (query.find("найди в интернете") >= 0) \
                or (query.find("найти в интернете") >= 0):
            self.search_in_internet(query)

        elif (query.find("прекратить работу") >= 0) or (query.find("прекрати работу") >= 0) \
                or (query.find("выключить ассистента") >= 0):
            self.close()

        elif (query.find("открыть файл hosts") >= 0) or (query.find("открой файл hosts") >= 0) \
                or (query.find("хостс") >= 0) or (query.find("открыть файл хост") >= 0):
            self.open_hosts()

        elif (query.find("увеличить громкость на") >= 0) or (query.find("уменьшить громкость") >= 0) \
                or (query.find("увеличь громкость на") >= 0) or (query.find("уменьшь громкость") >= 0):
            self.change_sound(query)

        elif (query.find("умножить") >= 0) or (query.find("умножь") >= 0):
            self.command_multy(query)


        else:
            self.base_text.setText("Команда не распознана")
            self.base_text.adjustSize()
            print("Команды не найдена")

    def open_task_manager(self):
        os.system("gnome-system-monitor")

    def open_settings(self):
        os.system("gnome-control-center")
        self.base_text.setText('Настройки системы открыты')
        self.base_text.adjustSize()

    def search_in_internet(self, query):
        final_word = ""
        new_string = query.split(" ")
        search = new_string[3:]
        for word in search:
            final_word += word + " "

        url = 'https://www.google.com/search?q=' + final_word

        webbrowser.open_new(url)

        self.base_text.setText('Ваш запрос выполнен')
        self.base_text.adjustSize()

    def open_hosts(self):
        os.system("gedit /etc/hosts")
        self.base_text.setText("Файл /etc/hosts открыт")
        self.base_text.adjustSize()

    def change_sound(self, query):
        command = query.split(" ")[0]
        current_volume = int(query.split(" ")[3])

        mix = alsaaudio.Mixer()  # инициализируем объект микшера
        our_volume = mix.getvolume()  # получили текущую громкость
        different_volume = 100 - our_volume[0]

        if command == "увеличить":
            if current_volume <= different_volume:
                vol = our_volume[0] + current_volume

                mix.setvolume(vol)
            else:
                mix.setvolume(100)
        else:
            if current_volume <= our_volume[0]:
                vol = our_volume[0] - current_volume
                mix.setvolume(vol)
            else:
                mix.setvolume(0)

        message = "Ваша громкость составляет: " + str(mix.getvolume()[0])
        self.base_text.setText(message)
        self.base_text.adjustSize()

    def command_multy(self, query):
        count = 0
        final_line = []
        new_line = query.split(" ")
        for word in new_line:
            count += 1
            if word == "умножить" or word == "умножь":
                final_line = new_line[count:]
                break

        first_number = int(final_line[0])
        second_number = int(final_line[2])

        res = first_number * second_number
        message = "Результат запроса: " + str(first_number) + " * " + str(second_number) + " = " + str(res)
        self.base_text.setText(message)
        self.base_text.adjustSize()


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
