import telebot
import os
import requests
import speech_recognition as sr
from pydub import AudioSegment
from config import TOKEN

# создаем объект бота
bot = telebot.TeleBot(TOKEN)

# обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне аудиосообщение, а я сделаю из него текст")

# создаем объект Recognizer
r = sr.Recognizer()

# функция для обработки входящих аудиосообщений
@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Отправляем "...typing" в индикаторе печати

    # получаем объект Audio объекта Voice сообщения
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))

    # создаем уникальное имя файла для каждого сообщения
    file_name = f"temp/{message.chat.id}_{message.message_id}.ogg"

    # сохраняем аудиофайл во временную папку
    os.makedirs('temp', exist_ok=True)  # создаем временную папку, если она не существует
    with open(file_name, 'wb') as f:
        f.write(file.content)

    # загружаем файл с помощью pydub
    ogg_audio = AudioSegment.from_file(file_name, format="ogg")

    # создаем уникальное имя файла для каждого сообщения
    wav_file = f"temp/{message.chat.id}_{message.message_id}.wav"

    # сохраняем файл в формате .wav
    ogg_audio.export(wav_file, format="wav")

    # открываем аудиофайл с помощью объекта AudioFile
    with sr.AudioFile(wav_file) as source:

        # записываем аудиоданные в объект AudioData
        audio_data = r.record(source)

    # распознаем речь с помощью Google Speech Recognition
    try:
        text = r.recognize_google(audio_data, language="ru-RU")
        # отправляем полученный текст пользователю
        bot.send_message(message.chat.id, text)
    except sr.UnknownValueError:
        bot.send_message(message.chat.id, "Речь не распознана")
    except sr.RequestError as e:
        bot.send_message(message.chat.id, "Ошибка сервиса распознавания речи {0}".format(e))

    # удаляем временные файлы (если они существуют)
    if os.path.exists(file_name):
        os.remove(file_name)
    if os.path.exists(wav_file):
        os.remove(wav_file)

# обработка остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я умею только переводить аудио в текст")        

# запускаем бота с возможностью обработки нескольких аудиосообщений
bot.infinity_polling()