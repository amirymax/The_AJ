import datetime
import sqlite3
from datetime import date
from brain import left_hemisphere as left


def write_daybook(text, day):
    con = sqlite3.connect('brain/all_data/all_things.db')
    cur = con.cursor()

    cur.execute('INSERT INTO daybook(day, time, speech) VALUES (?,?,?)',(*left.split_time_and_day(day), text))
    con.commit()
    con.close()


def search_on_google():
    left.search_on_google()


class GAFD:
    con = sqlite3.connect('brain/all_data/all_things.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM daybook')
    rows = cur.fetchall()
    day = []
    time = []
    speech = []

    for row in rows:
        day.append(row[0])
        time.append(row[1])
        speech.append(row[2])

    def print_all(self) -> None:
        for i in range(len(self.day)):
            print(self.day[i], self.time[i], self.speech[i])

    def get_all(self) -> list:
        return [self.day, self.time, self.speech]

    def get_by_date(self, date1: str, date2: str) -> None:

        start_date, end_date = left.to_date(date1, date2)
        indices = left.get_list_of_indices(start_date, end_date, self.day)
        try:
            assert indices != []
            for i in indices:
                print(self.day[i], self.time[i], self.speech[i])
        except AssertionError:
            print('Ягон запись нест (')

    cur.close()
    con.close()
