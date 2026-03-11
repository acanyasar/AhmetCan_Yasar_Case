"""
Insider Careers UI Test Suite
==============================
Steps run in order, sharing a single browser session (session-scoped driver).

Run with Chrome (default):
  python3 -m pytest tests/ui/ --browser=chrome -v


Run with Firefox:
    python3 -m pytest tests/ui/ --browser=firefox -v
"""

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QAJobsPage
from pages.lever_page import LeverPage


@pytest.mark.ui
class TestInsiderCareers:
    """End-to-end career flow on insiderone.com"""

    # ── Test 1 ────────────────────────────────────────────────────────────────
    def test_step1_home_page_loaded(self, driver):
        """Verify insiderone.com opens and all main blocks are present."""
        page = HomePage(driver)
        page.open_home()

        results = page.verify_main_blocks_loaded()
        missing = [block for block, visible in results.items() if not visible]

        assert not missing, (
            f"The following blocks were NOT found on the home page: {missing}"
        )

    # ── Test 2 ────────────────────────────────────────────────────────────────
    def test_step2_navigate_and_filter_jobs(self, driver):
        """
        Navigate to /careers/, click the Quality Assurance team link
        (which goes to jobs.lever.co), filter by Location=Istanbul,
        verify the jobs list is present.
        """
        careers = CareersPage(driver)
        careers.open_careers()
        careers.click_see_all_qa_jobs()

        jobs_page = QAJobsPage(driver)
        jobs_page.filter_by_location("Istanbul")
        jobs_page.filter_by_department("Quality Assurance")

        assert jobs_page.jobs_list_is_present(), (
            "Jobs list container is not visible after applying filters."
        )

    # ── Test 3 ────────────────────────────────────────────────────────────────
    def test_step3_jobs_content_validation(self, driver):
        """
        Verify every job card has:
          - Position containing 'QA' or 'Quality Assurance'
          - Department = 'Quality Assurance' (all jobs on this page are QA)
          - Location containing 'ISTANBUL' (Lever displays in uppercase)
        """
        jobs_page = QAJobsPage(driver)
        jobs = jobs_page.get_all_jobs()

        assert jobs, "No jobs found after filtering — cannot validate content."

        errors = []
        for i, job in enumerate(jobs, start=1):
            pos_upper = job["position"].upper()
            if "QA" not in pos_upper and "QUALITY ASSURANCE" not in pos_upper:
                errors.append(
                    f"Job #{i}: Position '{job['position']}' does not contain 'QA' or 'Quality Assurance'"
                )
            if "Quality Assurance" not in job["department"]:
                errors.append(
                    f"Job #{i}: Department '{job['department']}' does not contain 'Quality Assurance'"
                )
            if "ISTANBUL" not in job["location"].upper():
                errors.append(
                    f"Job #{i}: Location '{job['location']}' does not contain 'Istanbul'"
                )

        assert not errors, "Job content validation failed:\n" + "\n".join(errors)

    # ── Test 4 ────────────────────────────────────────────────────────────────
    def test_step4_view_role_redirects_to_lever(self, driver):
        """Click 'Apply' on the first job and verify it stays on Lever."""
        jobs_page = QAJobsPage(driver)
        jobs_page.click_view_role(index=0)

        # Handle possible new tab
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        lever = LeverPage(driver)
        current_url = lever.verify_lever_url()
        assert current_url, f"Lever URL verified: {current_url}"
