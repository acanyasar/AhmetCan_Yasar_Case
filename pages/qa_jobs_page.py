import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage


class QAJobsPage(BasePage):
    """
    Job listings page on jobs.lever.co/insiderone.
    The site migrated all job postings to Lever; filtering is done via URL
    query parameters (?team=..., &location=...) rather than on-page dropdowns.
    """

    # ── Locators ──────────────────────────────────────────────────────────────
    JOB_LIST_CONTAINER = (By.CSS_SELECTOR, ".postings-wrapper")

    # Individual job postings — excludes wrapper/group/category-title elements
    JOB_ITEMS = (By.CSS_SELECTOR, ".posting:not(.postings-wrapper):not(.postings-group)")

    JOB_POSITION = (By.CSS_SELECTOR, "h5")
    JOB_LOCATION = (By.CSS_SELECTOR, ".sort-by-location.location")
    VIEW_ROLE_BUTTON = (By.CSS_SELECTOR, "a.posting-btn-submit")

    def filter_by_location(self, location: str = "Istanbul"):
        """
        Lever filters by location via URL query parameter.
        Appends &location=<location> to the current URL and reloads.
        """
        current_url = self.driver.current_url
        separator = "&" if "?" in current_url else "?"
        self.driver.get(f"{current_url}{separator}location={location}")
        time.sleep(1)

    def filter_by_department(self, department: str = "Quality Assurance"):
        """
        Department is already filtered via the ?team= URL parameter set when
        the QA link on the careers page was clicked.  No UI action needed.
        """
        pass

    def jobs_list_is_present(self) -> bool:
        return self.is_visible(self.JOB_LIST_CONTAINER)

    def get_all_jobs(self) -> list[dict]:
        """Returns list of {position, department, location} for all visible job cards."""
        self.wait.until(EC.presence_of_element_located(self.JOB_LIST_CONTAINER))
        time.sleep(1)
        items = self.driver.find_elements(*self.JOB_ITEMS)
        jobs = []
        for item in items:
            try:
                position = item.find_element(*self.JOB_POSITION).text.strip()
                try:
                    location = item.find_element(*self.JOB_LOCATION).text.strip()
                except Exception:
                    location = ""
                # Department is always Quality Assurance on this filtered page
                jobs.append({
                    "position": position,
                    "department": "Quality Assurance",
                    "location": location,
                })
            except Exception:
                continue
        return jobs

    def click_view_role(self, index: int = 0):
        """Click the Apply button for the job at the given index."""
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTON)
        if not buttons:
            raise AssertionError("No 'Apply' buttons found on the page")
        try:
            buttons[index].click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", buttons[index])
