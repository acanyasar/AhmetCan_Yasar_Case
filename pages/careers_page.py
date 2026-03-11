from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    # The main careers page now hosts all team links including QA
    URL = "https://insiderone.com/careers/"

    # The QA team card links directly to Lever — identified by its href
    SEE_ALL_QA_JOBS_BUTTON = (By.CSS_SELECTOR, "a[href*='Quality']")

    def open_careers(self):
        self.open(self.URL)
        self.accept_cookies_if_present()

    def click_see_all_qa_jobs(self):
        # The QA card link is present in the DOM but inside a collapsed section;
        # use JS click to bypass the visibility requirement.
        element = self.find(self.SEE_ALL_QA_JOBS_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
