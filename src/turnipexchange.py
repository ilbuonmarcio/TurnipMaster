import time
import datetime
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class TurnipExchange():
    def __init__(self):
        pass

    def __get_driver(self, headless=True):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver

    def get_islands(self):
        print("Getting islands page...")
        driver = self.__get_driver()
        driver.get("https://turnip.exchange/islands")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, "note"))
        )
        page_source = driver.page_source
        driver.close()

        print("Parsing page...")
        soup = BeautifulSoup(page_source, 'html.parser')
        islands_available = soup.find_all('div', {'class': 'note'})

        islands = []
        for island_note in islands_available:
            island_top_note = island_note.findChildren('div', recursive=False)
            island_bottom_note = island_note.findChildren('p', recursive=False)

            code = island_note['data-turnip-code']
            name = island_top_note[0].findChild('h2').contents[0].strip()
            optype = 'buy' if datetime.datetime.now().weekday() == 6 else 'sell'
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

    def open_island(self, code):
        driver = self.__get_driver(headless=False)
        driver.get(f"https://turnip.exchange/island/{code}")


class Island():
    def __init__(self, code, name, optype, fruit, bell_price, emisphere, description, queue_length):
        self.code = code
        self.name = name
        self.optype = optype
        self.fruit = fruit
        self.bell_price = float(bell_price)
        self.emisphere = emisphere
        self.description = description
        self.queue_length = float(queue_length)

        if self.queue_length == 0:
            self.ratio = float("inf")
        else:
            self.ratio = self.bell_price / self.queue_length

    def __str__(self):
        return f"[c:{self.code}][t:{self.optype}][p:{self.bell_price}][q:{self.queue_length}][r:{self.ratio}]"


class IslandsFilter():
    def __init__(self):
        self.__filter_min_queue_length = 0
        self.__filter_max_queue_length = float("inf")
        self.__filter_min_bells = 0
        self.__filter_max_bells = float("inf")
        self.__filter_ignore_fruit = None
        self.__filter_emisphere = None

    def apply_filter(self, filter, value):
        print(f"Applying filter {filter}...")
        if filter == 'min_queue_length':
            if isinstance(value, int) and\
                value >= 0 and value <= float("inf") and\
                value <= self.__filter_max_queue_length:
                
                self.__filter_min_queue_length = value
            else:
                raise Exception(f"Invalid min_queue_length value: {value}")
        elif filter == 'max_queue_length':
            if isinstance(value, int) and\
                value >= 0 and value <= float("inf") and\
                value >= self.__filter_min_queue_length:

                self.__filter_max_queue_length = value
            else:
                raise Exception(f"Invalid max_queue_length value: {value}")

        elif filter == 'min_bells':
            if isinstance(value, int) and\
                value >= 0 and value <= float("inf") and\
                value <= self.__filter_max_bells:

                self.__filter_min_bells = value
            else:
                raise Exception(f"Invalid min_bells value: {value}")

        elif filter == 'max_bells':
            if isinstance(value, int) and\
                value >= 0 and value <= float("inf") and\
                    value >= self.__filter_min_bells:

                self.__filter_max_bells = value
            else:
                self.__filter_max_bells = value

        elif filter == 'ignore_fruit':
            if isinstance(value, str) and value in ['peach', 'apple', 'pear', 'cherry', 'orange']:
                self.__filter_ignore_fruit = value
            else:
                raise Exception(f"Invalid ignore_fruit value: {value}")

        elif filter == 'emisphere':
            if isinstance(value, str) and value in ['north', 'south']:
                self.__filter_emisphere = value
            else:
                raise Exception(f"Invalid emisphere value: {value}")

        else:
            raise Exception(f"Invalid filter name: {filter}")

        print(f"Added filter {filter} with value {value} successfully")

    def build(self, islands):
        print(f"Filtering by queue length ({len(islands)}) [{self.__filter_min_queue_length} <-> {self.__filter_max_queue_length}]")
        islands = list(filter(
            lambda island: island.queue_length >= self.__filter_min_queue_length and island.queue_length <= self.__filter_max_queue_length, islands
        ))

        print(f"Filtering by bells price ({len(islands)}) [{self.__filter_min_bells} <-> {self.__filter_max_bells}]")
        islands = list(filter(
            lambda island: island.bell_price >= self.__filter_min_bells and island.bell_price <= self.__filter_max_bells, islands
        ))

        print(f"Ignoring fruit ({len(islands)}) [{self.__filter_ignore_fruit}]")
        islands = list(filter(
            lambda island: island.fruit != self.__filter_ignore_fruit, islands
        ))

        print(f"Filtering by emisphere ({len(islands)}) [{self.__filter_emisphere}]")
        islands = list(filter(
            lambda island: self.__filter_emisphere is None or island.emisphere == self.__filter_emisphere, islands
        ))

        print(f"Islands after filters: {len(islands)}")
        return islands


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-queue-length', type=int, help="Set the minimum queue lenght (default: 0)")
    parser.add_argument('--max-queue-length', type=int, help="Set the maximum queue lenght (default: inf)")
    parser.add_argument('--min-bells', type=int, help="Set the minimum bells for turnip (default: 0)")
    parser.add_argument('--max-bells', type=int, help="Set the maximum bells for turnip (default: inf)")
    parser.add_argument('--ignore-fruit', type=str, help="Set the fruit to ignore (default: none) [avail: peach, pear, apple, cherry, orange]")
    parser.add_argument('--emisphere', type=str, help="Set the emisphere (default: none) [avail: north, south]")

    args = parser.parse_args()

    islands_filter = IslandsFilter()
    if args.min_queue_length is not None:
        islands_filter.apply_filter('min_queue_length', args.min_queue_length)
    if args.max_queue_length is not None:
        islands_filter.apply_filter('max_queue_length', args.max_queue_length)
    if args.min_bells is not None:
        islands_filter.apply_filter('min_bells', args.min_bells)
    if args.max_bells is not None:
        islands_filter.apply_filter('max_bells', args.max_bells)
    if args.ignore_fruit is not None:
        islands_filter.apply_filter('ignore_fruit', args.ignore_fruit)
    if args.emisphere is not None:
        islands_filter.apply_filter('emisphere', args.emisphere)

    tex = TurnipExchange()
    islands = tex.get_islands()

    islands = islands_filter.build(islands)

    [print(island) for island in islands]



    