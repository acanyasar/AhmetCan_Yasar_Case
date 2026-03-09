from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    URL = "https://insiderone.com/careers/quality-assurance/"

    # ── Locators ──────────────────────────────────────────────────────────────
    SEE_ALL_QA_JOBS_BUTTON = (
        By.XPATH,
        "//a[contains(text(),'See all QA jobs')] | "
        "//a[contains(@class,'btn') and contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'see all qa')]",
    )

    def open_careers(self):
        self.open(self.URL)

    def click_see_all_qa_jobs(self):
        self.scroll_into_view(self.SEE_ALL_QA_JOBS_BUTTON)
        self.click(self.SEE_ALL_QA_JOBS_BUTTON)
