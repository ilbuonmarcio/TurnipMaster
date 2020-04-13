import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class TurnipExchange():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_islands(self):
        self.driver.get("https://turnip.exchange/islands")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, "note"))
        )
        page_source = self.driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        islands_available = soup.find_all('div', {'class': 'note'})

        islands = []
        for island_note in islands_available:
            island_top_note = island_note.findChildren('div', recursive=False)
            island_bottom_note = island_note.findChildren('p', recursive=False)

            code = island_note['data-turnip-code']
            name = island_top_note[0].findChild('h2').contents[0].strip()
            optype = 'buy' if datetime.datetime.now().weekday() else 'sell'
            fruit = island_top_note[1].findChild('img', recursive=False)['src'].split('/')[-1:][0].replace('.png', '')
            tmp_element = island_top_note[1].findChild('div', {'class': 'flex'}, recursive=False)
            bell_price = tmp_element.findChild('p').contents[0].replace(' Bells', '')
            emisphere = island_top_note[1].findChild('p', recursive=False).contents[0].strip()
            description = island_bottom_note[0].contents[0].strip()
            queue_length = island_bottom_note[1].contents[0].strip().replace('Waiting: ', '')

            islands.append(
                Island(
                    code,
                    name,
                    optype,
                    fruit,
                    bell_price,
                    emisphere,
                    description,
                    queue_length
                )
            )

        return islands


class Island():
    def __init__(self, code, name, optype, fruit, bell_price, emisphere, description, queue_length):
        self.code = code
        self.name = name
        self.optype = optype
        self.fruit = fruit
        self.bell_price = int(bell_price)
        self.emisphere = emisphere
        self.description = description
        self.queue_length = int(queue_length)

        if self.queue_length == 0:
            self.ratio = float("inf")
        else:
            self.ratio = self.bell_price / self.queue_length

    def __str__(self):
        return f"[c:{self.code}][t:{self.optype}][p:{self.bell_price}][q:{self.queue_length}][r:{self.ratio}]"

    def __gt__(self, other):
        return self.ratio > other.ratio


if __name__ == "__main__":
    tex = TurnipExchange()
    islands = tex.get_islands()
    islands.sort(reverse=True)

    [print(island) for island in islands]



    