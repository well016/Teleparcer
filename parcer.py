import fake_useragent
import requests
from bs4 import BeautifulSoup
import re
import datetime




class Parser:
    def __init__(self,login, password):
        self.login=login
        self.password=password
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
    # Авторизация
    def auntification(self)-> str:
        payload = {
            'p_login': self.login,
            'p_pass': self.password
        }

        response = self.session.post('https://shelly.kpfu.ru/e-ksu/private_office.kfuscript', data=payload)
        parsed_url = re.search(r"document\.location\.href='([^']+)'", response.text).group(1)
        return parsed_url
    # Получили куки
    def get_cookies(self)-> dict:
        parsed_url=self.auntification()
        page_account=self.session.get(f'https://shelly.kpfu.ru/e-ksu/{parsed_url}')
        pattern = r"setCookie\('([^']+)', '([^']+)'"
        cookies = re.findall(pattern, page_account.text)
        # Преобразуем результат в словарь
        cookie_dict = {name: value for name, value in cookies}
        return cookie_dict






    # Функция для получения расписания на конкретный день недели
    def get_table_by_day(self,day_of_week):
        # Создание объекта BeautifulSoup для парсинга HTML-контента
        cookies=self.get_cookies()
        table=self.session.get('https://shelly.kpfu.ru/e-ksu/SITE_STUDENT_SH_PR_AC.shedule?p_menu=1',cookies=cookies)
        soup = BeautifulSoup(table.text, 'html.parser')

        # Поиск таблицы с расписанием
        schedule_table = soup.find('table', {'id': 'table-view'})
        if not schedule_table:
            return f"\u041d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430 \u0442\u0430\u0431\u043b\u0438\u0446\u0430 \u0441 \u0440\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435\u043c."

        # Поиск всех строк с днями недели
        days_rows = schedule_table.find_all('tr', {'valign': 'top'})
        current_day = None
        schedule = []

        # Перебор строк, чтобы найти нужный день и извлечь его расписание
        for row in days_rows:
            day_cell = row.find('td', {'class': 'day'})
            if day_cell:
                current_day = day_cell.get_text(strip=True)

            if current_day == day_of_week:
                lesson_cells = row.find_all('td')
                if len(lesson_cells) > 1:  # Проверка, чтобы убедиться, что это строка с предметом
                    time = lesson_cells[1].get_text(strip=True)
                    subject = lesson_cells[2].get_text(strip=True)
                    teacher = lesson_cells[4].get_text(strip=True)
                    building = lesson_cells[5].get_text(strip=True)
                    room = lesson_cells[7].get_text(strip=True)

                    # Добавляем найденные данные в расписание
                    schedule.append(
                        f"{time}: {subject}, \u043f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044c: {teacher}, \u0437\u0434\u0430\u043d\u0438\u0435: {building}, \u0430\u0443\u0434.: {room}")

        # Если расписание для указанного дня не найдено
        if not schedule:
            return f"\u041f\u0440\u0435\u0434\u043c\u0435\u0442\u044b \u043d\u0435 \u043d\u0430 \u043d\u0430\u0439\u0434\u0435\u043d\u044b \u0434\u043b\u044f {day_of_week}."

        # Возврат расписания в виде строки
        return "\n".join(schedule)


if __name__ == '__main__':
    a=Parser('RailRSabirov','QMT0Qk5mm7')
    print(a.get_table_by_day('Понедельник'))
    print()
    print(a.get_table_by_day('Вторник'))
    print()
    print(a.get_table_by_day('Среда'))



