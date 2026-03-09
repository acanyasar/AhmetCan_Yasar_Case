from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    # ── Locators ──────────────────────────────────────────────────────────────
    NAVBAR = (By.CSS_SELECTOR, "#navbarNavDropdown")
    HERO_SECTION = (By.CSS_SELECTOR, ".home-hero")
    HERO_TITLE = (By.CSS_SELECTOR, ".home-hero h1, .home-hero .hero-title")
    CUSTOMERS_SECTION = (By.CSS_SELECTOR, "#customers")
    TESTIMONIALS_SECTION = (By.CSS_SELECTOR, "#testimonial, .testimonials")
    PARTNERS_SECTION = (By.CSS_SELECTOR, ".joinus-section, .partners-section, [class*='partner']")
    FOOTER = (By.CSS_SELECTOR, "footer, .footer")
    LOGO = (By.CSS_SELECTOR, "nav .logo, nav img, .navbar-brand img, .navbar-brand")

    def open_home(self):
        self.open(self.URL)

    def verify_main_blocks_loaded(self) -> dict:
        """
        Checks that key page blocks are visible.
        Returns a dict {block_name: bool} for assertion reporting.
        """
        blocks = {
            "navbar": self.NAVBAR,
            "hero_section": self.HERO_SECTION,
            "footer": self.FOOTER,
            "logo": self.LOGO,
        }
        results = {}
        for name, locator in blocks.items():
            results[name] = self.is_visible(locator)
        return results
