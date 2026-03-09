from pages.base_page import BasePage


class LeverPage(BasePage):
    LEVER_URL_FRAGMENT = "lever.co"

    def verify_lever_url(self):
        """Assert that the current URL belongs to Lever (jobs.lever.co)."""
        self.wait_for_url_contains(self.LEVER_URL_FRAGMENT)
        current_url = self.driver.current_url
        assert self.LEVER_URL_FRAGMENT in current_url, (
            f"Expected URL to contain '{self.LEVER_URL_FRAGMENT}', got: {current_url}"
        )
        return current_url
