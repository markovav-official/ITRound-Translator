import json
from threading import Thread

import requests

url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

headers = {
    'x-rapidapi-key': "95f7464936mshaa12257cee57890p12e68fjsnd52d3eb4b848",
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}


class Language:
    ENGLISH = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    RUSSIAN = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


class Mode:
    EN_RU = 'EN_RU'
    RU_EN = 'RU_EN'
    AUTO = 'AUTO'


def detect_language(text):
    ru, en = 0, 0
    for item in text:
        if item in Language.ENGLISH:
            en += 1
        elif item in Language.RUSSIAN:
            ru += 1
        if ru + en > 20:
            break
    return Mode.EN_RU if en > ru else Mode.RU_EN


def translate_chunk(mode, text):
    if mode == Mode.RU_EN:
        querystring = {"q": text, "langpair": "ru|en", "de": "a@b.c", "onlyprivate": "0", "mt": "1"}
        query_res = requests.request("GET", url, headers=headers, params=querystring).text
        return json.loads(query_res)['responseData']['translatedText']
    if mode == Mode.EN_RU:
        querystring = {"q": text, "langpair": "en|ru", "de": "a@b.c", "onlyprivate": "0", "mt": "1"}
        query_res = requests.request("GET", url, headers=headers, params=querystring).text
        return json.loads(query_res)['responseData']['translatedText']


class Translator:
    def __init__(self):
        self.state = ''

    def translate(self, mode, text):
        Thread(target=self.translate_threaded, args=(mode, text)).start()

    def translate_threaded(self, mode, text):
        if mode == Mode.AUTO:
            mode = detect_language(text)
        def_text = 'Идет перевод...' if mode == Mode.RU_EN else 'Translation in progress...'
        self.state = def_text
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            paragraph_res = []
            chunks = []
            for word in paragraph.split():
                if len(chunks) == 0 or len(chunks[-1]) > 800:
                    chunks.append(word)
                else:
                    chunks[-1] += ' ' + word
            for chunk in chunks:
                paragraph_res.append(translate_chunk(mode, chunk))
            if self.state == def_text:
                self.state = ''
            self.state += ' '.join(paragraph_res) + '\n'
