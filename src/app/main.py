import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from src.utils.extractor import Extractor
from src.utils.scrapper import Scrapper

logger = logging.getLogger(__name__)

URL = "https://bez-kolejki.um.wroc.pl/#/"
SCRAPPER_OUTPUT = "passport_data.html"


def task() -> None:
    scrapper = Scrapper()
    scrapper.scrap_website(URL, SCRAPPER_OUTPUT)

    extractor = Extractor(SCRAPPER_OUTPUT)
    extractor.extract_passport_queue()


def main() -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(task, "interval", minutes=1)
    logger.info("Scheduler started. Press Ctrl+C to exit")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
