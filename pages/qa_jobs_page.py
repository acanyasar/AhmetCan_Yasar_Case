import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class QAJobsPage(BasePage):
    # ── Filter Locators ───────────────────────────────────────────────────────
    FILTER_LOCATION = (By.XPATH, "//span[contains(@class,'select2') and @id='select2-filter-by-location-container'] | //select[@id='filter-by-location']")
    FILTER_DEPARTMENT = (By.XPATH, "//span[contains(@class,'select2') and @id='select2-filter-by-team-container'] | //select[@id='filter-by-team']")

    # Select2 custom dropdowns
    SELECT2_LOCATION = (By.ID, "select2-filter-by-location-container")
    SELECT2_DEPARTMENT = (By.ID, "select2-filter-by-team-container")

    # Native selects (fallback)
    NATIVE_LOCATION_SELECT = (By.ID, "filter-by-location")
    NATIVE_DEPARTMENT_SELECT = (By.ID, "filter-by-team")

    # Dropdown search/options
    SELECT2_SEARCH_INPUT = (By.CSS_SELECTOR, ".select2-search__field")
    SELECT2_OPTIONS = (By.CSS_SELECTOR, ".select2-results__option")

    # Jobs list
    JOB_LIST_CONTAINER = (By.CSS_SELECTOR, "#jobs-list, .position-list")
    JOB_ITEMS = (By.CSS_SELECTOR, ".position-list-item, [class*='position-list'] li")
    JOB_POSITION = (By.CSS_SELECTOR, ".position-name, p.position-name")
    JOB_DEPARTMENT = (By.CSS_SELECTOR, ".position-department, span.position-department")
    JOB_LOCATION = (By.CSS_SELECTOR, ".position-location, span.position-location")
    VIEW_ROLE_BUTTON = (By.CSS_SELECTOR, ".btn-navy, a.btn[href*='lever'], a[class*='btn'][href*='lever']")

    def _select2_choose(self, trigger_locator, value: str):
        """Open a Select2 dropdown and pick an option matching value."""
        trigger = self.wait.until(EC.element_to_be_clickable(trigger_locator))
        trigger.click()
        time.sleep(0.5)
        # Type in the search box that appears
        search = self.wait.until(EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT))
        search.send_keys(value)
        time.sleep(0.5)
        options = self.driver.find_elements(*self.SELECT2_OPTIONS)
        for opt in options:
            if value.lower() in opt.text.lower():
                opt.click()
                return
        raise ValueError(f"Option '{value}' not found in Select2 dropdown")

    def _native_select_choose(self, select_locator, visible_text: str):
        element = self.find(select_locator)
        sel = Select(element)
        sel.select_by_visible_text(visible_text)

    def filter_by_location(self, location: str = "Istanbul, Turkey"):
        try:
            self._select2_choose(self.SELECT2_LOCATION, location)
        except Exception:
            self._native_select_choose(self.NATIVE_LOCATION_SELECT, location)
        time.sleep(1)

    def filter_by_department(self, department: str = "Quality Assurance"):
        try:
            self._select2_choose(self.SELECT2_DEPARTMENT, department)
        except Exception:
            self._native_select_choose(self.NATIVE_DEPARTMENT_SELECT, department)
        time.sleep(1)

    def get_all_jobs(self) -> list[dict]:
        """Returns list of {position, department, location} for all visible job cards."""
        self.wait.until(EC.presence_of_element_located(self.JOB_LIST_CONTAINER))
        time.sleep(1)
        items = self.driver.find_elements(*self.JOB_ITEMS)
        jobs = []
        for item in items:
            try:
                position = item.find_element(*self.JOB_POSITION).text.strip()
                department = item.find_element(*self.JOB_DEPARTMENT).text.strip()
                location = item.find_element(*self.JOB_LOCATION).text.strip()
                jobs.append(
                    {"position": position, "department": department, "location": location}
                )
            except Exception:
                continue
        return jobs

    def jobs_list_is_present(self) -> bool:
        return self.is_visible(self.JOB_LIST_CONTAINER)

    def click_view_role(self, index: int = 0):
        """Click the View Role button for the job at the given index."""
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTON)
        if not buttons:
            raise AssertionError("No 'View Role' buttons found on the page")
        buttons[index].click()
