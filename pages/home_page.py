from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    # ── Locators ──────────────────────────────────────────────────────────────
    NAVBAR = (By.CSS_SELECTOR, "#navigation")
    HERO_SECTION = (By.CSS_SELECTOR, ".homepage-hero")
    FOOTER = (By.CSS_SELECTOR, "#footer, section#footer, footer")
    LOGO = (By.CSS_SELECTOR, ".navbar-brand, #navigation img, nav img[src*='logo']")

    def open_home(self):
        self.open(self.URL)
        self.accept_cookies_if_present()

    def verify_main_blocks_loaded(self) -> dict:
        """
        Checks that key page blocks are present in the DOM.
        Uses presence rather than visibility — JS-animated sections and canvas
        backgrounds may not satisfy Selenium's strict visibility check even
        when visually rendered.
        Returns a dict {block_name: bool} for assertion reporting.
        """
        from selenium.webdriver.support import expected_conditions as EC
        blocks = {
            "navbar": self.NAVBAR,
            "hero_section": self.HERO_SECTION,
            "footer": self.FOOTER,
            "logo": self.LOGO,
        }
        results = {}
        for name, locator in blocks.items():
            try:
                self.wait.until(EC.presence_of_element_located(locator))
                results[name] = True
            except Exception:
                results[name] = False
        return results
