import fake_useragent
import requests
from bs4 import BeautifulSoup
import re
#Создаем сессию
session = requests.Session()
user = fake_useragent.UserAgent().random
# Авторизация
payload = {
    'p_login': 'RailRSabirov',
    'p_pass': 'QMT0Qk5mm7'
}

# Авторизация
def auntification(login: str,password: str):
    payload = {
        'p_login': login,
        'p_pass': password
    }
    headers = {
        "User-Agent": user,
    }
    response = session.post('https://shelly.kpfu.ru/e-ksu/private_office.kfuscript', data=payload, headers=headers)
    parsed_url = re.search(r"document\.location\.href='([^']+)'", response.text).group(1)
    return parsed_url
print(auntification(login='RailRSabirov',password='QMT0Qk5mm7'))

def get_cookies():
    pass
page_account=session.get(f'https://shelly.kpfu.ru/e-ksu/{parsed_url}', headers=headers)

pattern = r"setCookie\('([^']+)', '([^']+)'"

# Поиск всех совпадений
cookies = re.findall(pattern, page_account.text)

# Преобразуем результат в словарь
cookie_dict = {name: value for name, value in cookies}


print(f'Вот куки {session.cookies}')



print('Авторизация успешна' if response.ok else 'Авторизация не удалась')


table=session.get('https://shelly.kpfu.ru/e-ksu/SITE_STUDENT_SH_PR_AC.shedule?p_menu=1', headers=headers, cookies=cookie_dict)


