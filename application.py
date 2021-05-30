import datetime
import os

import PySimpleGUI as sg

from Sirius_IT_Round.task import Task
from Sirius_IT_Round.translate import Translator
from Sirius_IT_Round.windows_clipboard import to_clipboard, get_clipboard


class Application:
    def __init__(self):
        self.layout = [
            [
                sg.Submit(button_text='Авто', key="mode=AUTO", disabled=True),
                sg.Submit(button_text='Русский -> Английский', key="mode=RU_EN"),
                sg.Submit(button_text='Английский -> Русский', key="mode=EN_RU")
            ],
            [
                sg.Multiline(size=(150, 20), key='Input')
            ],
            [
                sg.Submit(button_text='Вставить из буфера', key="Paste"),
                sg.Submit(button_text='Очистить', key="Clear")
            ],
            [
                sg.Multiline(size=(150, 20), key='Output', disabled=True)
            ],
            [
                sg.Submit(button_text='Скопировать', key="Copy")
            ],
        ]
        self.window = sg.Window('UniversalTranslator', self.layout, icon=os.path.join('data', 'icon.ico'),
                                text_justification='c', element_justification='c')
        self.window.finalize()

        self.mode = 'AUTO'
        self.last_state = ''
        self.last_update = datetime.datetime.now()
        self.translated = True
        self.translator = Translator()

        self.task = Task(self.work, ())
        self.task.start_runner()

        self.run_event_loop()

    def run_event_loop(self):
        while True:
            event, values = self.window.read()
            if event is None:
                break
            elif event.startswith('mode='):
                self.mode = event.split('mode=')[1]
                for btn in self.layout[0]:
                    if event == btn.Key:
                        self.window[btn.Key].update(disabled=True)
                    else:
                        self.window[btn.Key].update(disabled=False)
            elif event == 'Clear':
                self.window["Input"].update(value='')
                self.window["Output"].update(value='')
            elif event == 'Paste':
                self.window["Input"].update(value=get_clipboard())
            elif event == 'Copy':
                to_clipboard(self.window["Output"].get())
        os._exit(0)

    def work(self):
        input_text = self.window["Input"].get().strip()
        check_state = input_text + self.mode
        if input_text.strip() == '':
            self.last_state = ''
            if self.window["Output"].get().strip() != '':
                self.window["Output"].update(value='')
            if self.translator.state.strip() != '':
                self.translator.state = ''
            return
        if check_state != self.last_state:
            self.last_state = check_state
            self.last_update = datetime.datetime.now()
            self.translated = False
        if not self.translated and (datetime.datetime.now() - self.last_update).total_seconds() > 0.5:
            self.translator.translate(self.mode, input_text)
            self.translated = True
        if self.window["Output"].get().strip() != self.translator.state.strip():
            self.window["Output"].update(value=self.translator.state)


app = Application()
