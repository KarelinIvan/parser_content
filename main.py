import urllib.request
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, site):
        self.site = site

    def scrape(self):
        try:
            # Открываем соединение и получаем HTML страницы
            r = urllib.request.urlopen(self.site)
            html = r.read()
            parser = "html.parser"
            sp = BeautifulSoup(html, parser)

            # Переменная для хранения найденных уникальных ссылок
            urls_found = []

            for tag in sp.find_all("a", href=True):  # Ищем теги <a> с атрибутом href
                url = tag["href"]

                # Пропускаем сторонние домены и оставляем только внутренние новости
                if url.startswith("http") and "news.mail.ru" not in url:
                    continue
                if url.startswith("/"):
                    url = "https://news.mail.ru" + url  # Преобразуем относительные ссылки

                # Фильтруем только новости (обычно содержат /news/, /society/, /politics/ и т.д.)
                news_keywords = ["/news/", "/society/", "/politics/", "/incident/", "/economy/", "/sport/"]
                if any(keyword in url for keyword in news_keywords) and url not in urls_found:
                    urls_found.append(url)
                    print(url)

            print(f"\nВсего найдено {len(urls_found)} новостных ссылок.")

        except Exception as e:
            print("Произошла ошибка при парсинге:", e)

# Запуск скрапера
news = "https://news.mail.ru/"
Scraper(news).scrape()