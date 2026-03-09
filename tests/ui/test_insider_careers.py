"""
Insider Careers UI Test Suite
==============================
Steps run in order, sharing a single browser session (session-scoped driver).

Run with Chrome (default):
    pytest tests/ui/ --browser=chrome -v

Run with Firefox:
    pytest tests/ui/ --browser=firefox -v
"""

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QAJobsPage
from pages.lever_page import LeverPage


@pytest.mark.ui
class TestInsiderCareers:
    """End-to-end career flow on insiderone.com"""

    # ── Step 1 ────────────────────────────────────────────────────────────────
    def test_step1_home_page_loaded(self, driver):
        """Verify insiderone.com opens and all main blocks are visible."""
        page = HomePage(driver)
        page.open_home()

        results = page.verify_main_blocks_loaded()
        missing = [block for block, visible in results.items() if not visible]

        assert not missing, (
            f"The following blocks were NOT visible on the home page: {missing}"
        )

    # ── Step 2 ────────────────────────────────────────────────────────────────
    def test_step2_navigate_and_filter_jobs(self, driver):
        """
        Navigate to /careers/quality-assurance/, click 'See all QA jobs',
        filter by Location=Istanbul,Turkey and Department=Quality Assurance,
        verify the jobs list is present.
        """
        careers = CareersPage(driver)
        careers.open_careers()
        careers.click_see_all_qa_jobs()

        jobs_page = QAJobsPage(driver)
        jobs_page.filter_by_location("Istanbul, Turkey")
        jobs_page.filter_by_department("Quality Assurance")

        assert jobs_page.jobs_list_is_present(), (
            "Jobs list container is not visible after applying filters."
        )

    # ── Step 3 ────────────────────────────────────────────────────────────────
    def test_step3_jobs_content_validation(self, driver):
        """
        Verify every job card has:
          - Position containing 'Quality Assurance'
          - Department containing 'Quality Assurance'
          - Location containing 'Istanbul, Turkey'
        """
        jobs_page = QAJobsPage(driver)
        jobs = jobs_page.get_all_jobs()

        assert jobs, "No jobs found after filtering — cannot validate content."

        errors = []
        for i, job in enumerate(jobs, start=1):
            if "Quality Assurance" not in job["position"]:
                errors.append(
                    f"Job #{i}: Position '{job['position']}' does not contain 'Quality Assurance'"
                )
            if "Quality Assurance" not in job["department"]:
                errors.append(
                    f"Job #{i}: Department '{job['department']}' does not contain 'Quality Assurance'"
                )
            if "Istanbul, Turkey" not in job["location"]:
                errors.append(
                    f"Job #{i}: Location '{job['location']}' does not contain 'Istanbul, Turkey'"
                )

        assert not errors, "Job content validation failed:\n" + "\n".join(errors)

    # ── Step 4 ────────────────────────────────────────────────────────────────
    def test_step4_view_role_redirects_to_lever(self, driver):
        """Click 'View Role' on the first job and verify redirect to Lever application form."""
        jobs_page = QAJobsPage(driver)
        jobs_page.click_view_role(index=0)

        # Handle possible new tab
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        lever = LeverPage(driver)
        current_url = lever.verify_lever_url()
        assert current_url, f"Lever URL verified: {current_url}"
