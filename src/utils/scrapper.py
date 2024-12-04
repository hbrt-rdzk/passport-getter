import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class Scrapper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

    def scrap_website(self, url: str, output_file: str) -> None:
        logger.info("Extraction started")
        try:
            self.driver.get(url)
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--dark.v-size--default.primary",
                    )
                )
            )
            button.click()

            button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[.//div[text()='COM VI przy ul. Legnickiej 58 (Magnolia Park)']]",
                    )
                )
            )
            button.click()

            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[text()='DALEJ']]")
                )
            )
            button.click()

            self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button.queue-button.wrap-btn.button-with-right-icon.v-btn.v-btn--block.v-btn--outlined.theme--light.v-size--large",
                    )
                )
            )
            next_page_content = self.driver.page_source

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(next_page_content)

            logger.info(f"Data scraped and saved to {output_file}")

        except Exception as e:
            logger.error(f"Error occured: {e}")

        finally:
            self.driver.quit()
