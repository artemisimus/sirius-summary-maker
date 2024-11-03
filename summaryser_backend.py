import requests
import sys
from urllib.parse import urlencode
import os
import whisper
import random
import string
import ollama
from moviepy.editor import VideoFileClip

final_link = ''

desired_model = 'llama3.2:3b'

def to_llama(question_text):
    response = ''

    start_char = 0
    end_char = 2000

    while(start_char <= len(question_text)):
        response += ollama.chat(model=desired_model, messages=[
            {
                'role': 'system',
                'content': 'Создай сжатую версию материала, который отправит тебе пользователь. Не пиши в ответе ничего, кроме пересказа',
            },
            {
                'role': 'user',
                'content': question_text[start_char : end_char],
            },
        ])['message']['content'] + ' '

        start_char += 1990
        end_char += 1990

    return response 

def get_href(public_link):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    final_url = base_url + urlencode(dict(public_key=public_link))
    response = requests.get(final_url)
    parse_href = response.json()['href']
    return parse_href


def download_files(url, userid):
    
    currient_folder = os.getcwd()
    destination_folder = os.path.join(currient_folder, "download_files")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    start_filename = url.find('filename=')
    end_filename = url[start_filename:].find('&')
    end_name = start_filename + end_filename
    filename = f'{userid}.mp4'      
    download_url = requests.get(url)
    final_link = os.path.join(destination_folder, filename)
    with open(final_link, 'wb') as ff:
        ff.write(download_url.content)
    
    print("Скачан файл: ", filename)
    
    return final_link

def extract_audio(file_path, userid):
    const_path = f'audio/{userid}.mp3'
    clip = VideoFileClip(file_path)
    clip.audio.write_audiofile(const_path)
    return const_path

def to_whisper(file_path):
    whisper_model = whisper.load_model("small")

    transcribed_text = whisper_model.transcribe(file_path)
    return transcribed_text['text']

def show_summary(userid):
    print(f'answers/{userid}.txt :\n\n')
    with open(f'answers/{userid}.txt', 'r') as answer:
        print(answer.read())


def serve(ya_disk_link):
    userid = ''
    for i in range(0, 10):
        userid += random.choice(string.ascii_letters)

    if not os.path.exists('audio'):
        os.mkdir('audio')
    if not os.path.exists('text'):
        os.mkdir('text')
    if not os.path.exists('answers'):
        os.mkdir('answers')

    file_path = download_files(get_href(ya_disk_link), userid)
    audio_file_path = extract_audio(file_path, userid)
    with open(f'text/{userid}.txt', 'w') as text_file:
        text_file.write(to_whisper(audio_file_path))

    with open(f'text/{userid}.txt', 'r') as text_file:
        with open(f'answers/{userid}.txt', 'w') as answer:
            answer.write(to_llama(text_file.read()))

    show_summary(userid)
    

serve(sys.argv[1])
