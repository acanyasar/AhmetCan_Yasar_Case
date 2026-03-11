import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


class BasePage:
    TIMEOUT = 15
    COOKIE_ACCEPT_BTN = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn, #wt-cli-accept-btn")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            # Fixed navbar or overlay is blocking — fall back to JS click
            self.driver.execute_script("arguments[0].click();", element)

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def take_screenshot(self, name: str = "screenshot"):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join("screenshots", f"{name}_{timestamp}.png")
        self.driver.save_screenshot(path)
        return path

    def scroll_into_view(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def accept_cookies_if_present(self):
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)
            )
            btn.click()
        except Exception:
            pass  # No cookie banner present

    def wait_for_url_contains(self, fragment: str):
        self.wait.until(EC.url_contains(fragment))
