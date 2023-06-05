from datetime import date, datetime


def split_time_and_day(day: str) -> list:
    day = day.lower()
    time = ''
    if ':' in day:
        i = day.index(':')
        time = day[i - 2] + day[i - 1] + ':' + day[i + 1] + day[i + 2]
        day = day.replace(time, '')
    if 'имруз' in day:
        day = day.replace('имруз', date.today().strftime('%d.%m.%Y'))
    try:
        day = datetime.strptime(day, '%d.%m.%Y')
    except ValueError:
        print("Времяра безеб навишти")
    return [day, time]


def to_date(date1: str, date2: str) -> list:
    date1 = date1.replace(' ', '')
    date2 = date2.replace(' ', '')
    date1 = datetime.strptime(date1, '%d.%m.%Y')
    date2 = datetime.strptime(date2, '%d.%m.%Y')
    return [date1, date2]


def get_list_of_indices(date1: datetime, date2: datetime, days: list) -> list:
    indices = []
    for i in range(len(days)):
        day = datetime.strptime(days[i].replace(' ', ''), '%d.%m.%Y')
        if date1 <= day <= date2:
            indices.append(i)

    return indices


def search_on_google():
    import requests
    from bs4 import BeautifulSoup

    search_query = input("Чи бковем?\n::::\n\t  ")

    url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.find_all("div", class_="g")

    for result in results:
        title_elem = result.find("h3", class_="LC20lb")
        link_elem = result.find("a")
        description_elem = result.find("div", class_="VwiC3b")

        if title_elem is not None:
            title = title_elem.get_text()
            print(f"Титул: {title}")

        if link_elem is not None:
            link = link_elem["href"]
            print(f"Ссылка: {link}")

        if description_elem is not None:
            description = description_elem.get_text()
            print(f"Да бораш: {description}")

        print("\n")
