import miniaudio
import array

import pyaudio
import numpy as np
import whisper
import subprocess
import wave
import webbrowser

import pymorphy3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import os

buffer_chunks = []

def choose_device():
    devices = miniaudio.Devices()
    print("Доступнве устройства:")
    captures = devices.get_captures()
    for d in enumerate(captures):
        print("{num} = {name}".format(num=d[0], name=d[1]['name']))
    choice = int(input("Выберете устройство записи: "))
    return captures[choice]

def record_to_buffer():
    _ = yield
    while True:
        data = yield
        print(".", end="", flush=True)
        buffer_chunks.append(data)

def get_audio():
    """Запись аудио"""
    capture = miniaudio.CaptureDevice(buffersize_msec=1000, sample_rate=44100, device_id=choose_device()['id'])
    generator = record_to_buffer()
    next(generator)
    capture.start(generator)
    input('Надмите Enter для остановки записи')
    capture.stop()
    buffer = b"".join(buffer_chunks)
    samples = array.array('h')
    samples.frombytes(buffer)
    sound = miniaudio.DecodedSoundFile('command', capture.nchannels, capture.sample_rate, capture.format, samples)
    miniaudio.wav_write_file('command.wav', sound)


def recognize_speech():   
    """Распознование речи""" 
    model = whisper.load_model('tiny')
    transcription = model.transcribe(r"command.wav", fp16=False, language='russian') 
    return transcription

def preprocess_text(transcription):
    """Обработка текста"""
    tokens = word_tokenize(transcription)
    morph = pymorphy3.MorphAnalyzer()    
    tokens = [morph.parse(token)[0].normal_form for token in tokens if token.isalnum() and not token.isdigit()]
    tokens = [token for token in tokens if token not in stopwords.words('russian')]
    return tokens

def command(tokens):
    if 'найти' in tokens:
        webbrowser.open('https://ya.ru/')
    elif 'видео' in tokens:
        webbrowser.open('https://rutube.ru/')
    elif 'записать' in tokens:
        subprocess.run(['notepad.exe'])
    elif 'поговорить' in tokens:
        webbrowser.open('https://web.telegram.org/a/')
    else:
        print('Неизвестная команда!')


if __name__ == '__main__':
    get_audio()
    transcription = recognize_speech()
    print(f'Текст команды: {transcription['text']}')

    tokens = preprocess_text(transcription['text'])
    print(f'Леммы команды: {tokens}')
    command(tokens)

    os.remove('command.wav')
