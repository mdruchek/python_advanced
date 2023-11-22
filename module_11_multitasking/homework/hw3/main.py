import logging
import random
import threading
import time
from typing import List

START_TICKETS: int = 10
TOTAL_TICKETS: int = START_TICKETS
TOTAL_PLACES: int = 100
NUMBER_PRINTED_TICKETS_AT_TIME = 6

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            if TOTAL_TICKETS <= 4:
                time.sleep(1)
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.name = 'Director'
        self.sem: threading.Semaphore = semaphore
        self.tickets_printed: int = 0
        logger.info(f'{self.name} started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        ticket_printing_available = True
        while is_running and ticket_printing_available:
            if TOTAL_TICKETS <= 4:
                with self.sem:
                    for _ in range(NUMBER_PRINTED_TICKETS_AT_TIME):
                        if self.tickets_printed + START_TICKETS == TOTAL_PLACES:
                            ticket_printing_available = False
                            break
                        self.tickets_printed += 1
                        TOTAL_TICKETS += 1
                        logger.info(f'{self.name} printed one;  {TOTAL_TICKETS} total')
        logger.info(f'{self.name} {self.tickets_printed} tickets')


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    cinema: List[Seller | Director] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        cinema.append(seller)

    director = Director(semaphore)
    director.start()
    cinema.append(director)

    for employee in cinema:
        employee.join()


if __name__ == '__main__':
    main()
