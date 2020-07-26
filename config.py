from datetime import date

import requests
from bs4 import BeautifulSoup

import database

TOKEN = 'your-token'


def update_table():
    conn = database.create_connection('bod.db')
    sql = 'DELETE FROM weather WHERE 1'
    conn.execute(sql)
    conn.commit()
    complete_url = "https://yandex.kg/weather/yaroslavl/month"
    response = requests.get(complete_url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find('div', attrs={'class': 'climate-calendar'})
    days = table.find_all('div', attrs={'class': 'climate-calendar-day__detailed-container-center'})
    purchases = []
    for day in days:
        try:
            day_day = day.find('h6', attrs={'class': 'climate-calendar-day__detailed-day'})
            day_temp = day.find('span', attrs={'class': 'temp__value'})
            table = day.find('table', attrs={'class': 'climate-calendar-day__detailed-data-table'})
            table_tr = table.find('tr')
            day_dav = table_tr.find_all('td')[1]
            day_vla = table_tr.find_all('td')[3]
            purchases.append((date.today(), day_day.text, day_temp.text, day_dav.text, day_vla.text))
        except Exception as e:
            print(e)
    conn.executemany('INSERT INTO weather VALUES (?,?,?,?,?)', purchases)
    conn.commit()


def get_weather(date_weather, updated=False):
    conn = database.create_connection('bod.db')
    cursor = conn.execute("SELECT * from weather WHERE date LIKE ? LIMIT 1",
                          (date_weather + '%',))
    rows = cursor.fetchall()
    if len(rows):
        row = rows[0]
        if row[0] == str(date.today()):
            return """Дата: {},\nТемпература воздуха: {},\nДавление: {},\nВлажность: {}""".format(row[1], row[2],
                                                                                                    row[3], row[4])
    if not updated:
        update_table()
        return get_weather(date_weather, True)
    return 'Нет такой даты'

# print(get_weather('2qs'))
