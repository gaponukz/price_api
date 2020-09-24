from bot import TemplateBot
from bs4 import BeautifulSoup
from time import sleep

from fastapi import FastAPI
# pip install -r libs.txt

class ParserBot(TemplateBot):
    def parse(self, url: str) -> float:
        self.driver.get(url)
        self.protected_sleep(1.5)

        while True:
            html = BeautifulSoup(self.driver.page_source, 'html.parser')

            yield (
                html.find('div', {
                    'class': "tv-symbol-price-quote__value js-symbol-last"
                }).text
            )

if __name__ == "__main__":
    app = FastAPI()
    parser = ParserBot(show = False)
    price = parser.parse('https://ru.tradingview.com/symbols/EURUSD/')

    @app.get("/")
    def read_root():
        return {"price": price.__next__()}