import requests
from urllib.parse import urlencode
import os
import whisper
import random
import string

final_link = ''


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
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f'extract/{userid}.mp3')
    return f'audio/{userid}.mp3'

def to_whisper(file_path):
    whisper_model = whisper.load_model("small")

    transcribed_text = whisper_model.transcribe(file_path)
    return transcribed_text['text']


def serve(ya_disk_link):
    username = ''
    for i in range(0, 10):
        username += random.choice(string.ascii_letters)
    os.makedirs('audio')
    os.makedirs('text')
    file_path = download_files(get_href(ya_disk_link), userid)
    audio_file_path = extract_audio(file_path, userid)
    with open(f'text/{uerid}.txt', 'w') as text_file:
        text_file.write(to_whisper(audio_file_path))

#serve('https://disk.yandex.ru/i/ASpAgpoBjGggbw')
