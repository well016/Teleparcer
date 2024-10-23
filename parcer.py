import requests
from bs4 import BeautifulSoup

payload = {
    'p_login': 'RailRSabirov',
    'p_pass': 'QMT0Qk5mm7'
}
response = requests.post('https://shelly.kpfu.ru/e-ksu/private_office.kfuscript', data=payload)
if "document.location.href" in response.text:
    # Извлекаем URL для перенаправления
    start = response.text.find("document.location.href='") + len("document.location.href='")
    end = response.text.find("'", start)
    redirect_url = response.text[start:end]

    # Выполняем запрос на новый URL
    new_response = requests.get(f'https://shelly.kpfu.ru/e-ksu/{redirect_url}')
else:
    print("Нет перенаправления или произошла ошибка")
soup = BeautifulSoup(new_response.content, )
print(soup)
adres=soup.find_all('')
print(adres)







