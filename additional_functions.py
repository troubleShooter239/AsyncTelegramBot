from random import choice, randint
from requests import get
from bs4 import BeautifulSoup as bs
import lxml


answers = {
    "привет": ("Привет!", "Здравствуйте!", "Вечер в хату."),
    "пока": ("Пока!", "Пока-пока!", "До свидания!", "Увидимся!")
}


def get_insult() -> str:
    """
    Возвращаем случайное оскорбление
    """
    with open('insults.txt', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    return choice(lines)


def get_joke() -> str:
    """
    Возвращаем случайный анекдот
    """
    url_dict = {
        "https://anekdoty.ru/pro-hoholov/": 4,
        "https://anekdoty.ru/pro-programmistov/": 12,
        "https://anekdoty.ru/pro-gitlera/": 3,
        "https://anekdoty.ru/pro-negrov/": 11,
        "https://anekdoty.ru/pro-seks/": 22,
        "https://anekdoty.ru/cherniy-yumor/": 6,
        "https://anekdoty.ru/pro-mamu/": 15,
        "https://anekdoty.ru/detskie/": 26,
        "https://anekdoty.ru/pro-armyan/": 7,
        "https://anekdoty.ru/pro-gruzinov/": 19,
        "https://anekdoty.ru/pro-klounov/": 3,
        "https://anekdoty.ru/samye-smeshnye/": 20,
        "https://anekdoty.ru/tupo-no-smeshno/": 28,
        "https://anekdoty.ru/korotkie/": 14,
        "https://anekdoty.ru/pro-invalidov/": 2,
        "https://anekdoty.ru/pro-mobilizaciyu/": 5,
        "https://anekdoty.ru/pro-vovochku/": 57,
        "https://anekdoty.ru/pro-podrostkov/": 2,
        "https://anekdoty.ru/poshlye-anekdoty/": 25,
        "https://anekdoty.ru/pro-shtirlica/": 22,
        "https://anekdoty.ru/pro-geev/": 8,
        "https://anekdoty.ru/pro-zhenu/": 41,
        "https://anekdoty.ru/pro-narkomanov/": 24,
        "https://anekdoty.ru/pro-evreev/": 70,
        "https://anekdoty.ru/pro-vzroslyh/": 7,
    }

    rand_key = choice(list(url_dict))
    rand_page = randint(1, url_dict[rand_key])

    if rand_page != 1:
        page = get(rand_key + str(rand_page) + '/')  # Собираем html-код со страницы
        page = bs(page.text, 'lxml')  # Делаем парсинг страницы при помощи lxml
        jokes = [i.text for i in page.find_all('p')]  # Собираем все анекдоты в один список
    else:
        page = get(rand_key)  # Собираем html-код со страницы
        page = bs(page.text, 'lxml')  # Делаем парсинг страницы при помощи lxml
        jokes = [i.text for i in page.find_all('p')]  # Собираем все анекдоты в один список

    return choice(jokes)  # Возвращаем список


def get_news() -> str:
    """
    Возвращаем новости
    """
    page = get('https://3dnews.ru/news')
    page = bs(page.text, 'lxml')
    header = [i.text for i in page.find_all('h1')]
    news = [i. text for i in page.find_all('p')]
    news_dict = dict(zip(header, news))

    return news_dict.get(choice(header))


def get_weather(city: str, weather_token: str) -> str:
    """
    Возвращаем прогноз погоды для введенного города
    """
    try:
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        page = get(f'https://api.openweathermap.org/data/2.5/weather?q='
                   f'{city}&appid={weather_token}&units=metric').json()

        city = page['name']
        temp = page['main']['temp']
        humidity = page["main"]["humidity"]
        wind = page["wind"]["speed"]
        weather_description = page["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        return f'Город: {city}\n' \
               f'Температура: {temp} ℃ {wd}\n' \
               f'Влажность: {humidity}%\n' \
               f'Скорость ветра: {wind}м/с'

    except:
        return 'Название города введено некорректно.'


def get_compliment() -> str:
    """
    Возвращаем случайный комплимент
    """
    with open('compliments.txt', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    return choice(lines)
