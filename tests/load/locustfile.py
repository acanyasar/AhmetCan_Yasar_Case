"""
Load Test — n11.com Search Module
===================================
Scenarios:
  1. KeywordSearchUser  — searches for a common product keyword ("laptop")
  2. CategorySearchUser — searches for a category term ("telefon")
  3. EmptySearchUser    — submits an empty search (edge/negative scenario)

Run (1 user, 60 seconds):
    locust -f tests/load/locustfile.py \\
           --headless -u 1 -r 1 --run-time 60s \\
           --host https://www.n11.com

Locust web UI (interactive):
    locust -f tests/load/locustfile.py --host https://www.n11.com
    # then open http://localhost:8089
"""

from locust import HttpUser, TaskSet, task, between, events


# ── Shared search helper ──────────────────────────────────────────────────────

def do_search(client, keyword: str):
    """
    Simulates a user typing a keyword into the n11.com header search box
    and loading the results page.

    n11.com uses a GET request to /arama/ with ?q=<keyword> for search results.
    """
    params = {"q": keyword}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    with client.get(
        "/arama/",
        params=params,
        headers=headers,
        name=f"/arama/?q={keyword}",
        catch_response=True,
    ) as response:
        if response.status_code == 200:
            if "arama" in response.url or keyword.lower() in response.text.lower():
                response.success()
            else:
                response.failure(
                    f"Search results page did not contain expected content for '{keyword}'"
                )
        else:
            response.failure(
                f"Search request failed with status {response.status_code}"
            )


# ── Scenario 1: Keyword search ────────────────────────────────────────────────

class KeywordSearchTasks(TaskSet):
    """Searches for a common product keyword and verifies results page loads."""

    def on_start(self):
        """Load the homepage before starting tasks."""
        self.client.get("/", name="GET /homepage")

    @task(3)
    def search_laptop(self):
        do_search(self.client, "laptop")

    @task(2)
    def search_headphones(self):
        do_search(self.client, "kulaklık")

    @task(1)
    def search_shoes(self):
        do_search(self.client, "ayakkabı")


class KeywordSearchUser(HttpUser):
    tasks = [KeywordSearchTasks]
    wait_time = between(1, 3)
    weight = 3


# ── Scenario 2: Category search ───────────────────────────────────────────────

class CategorySearchTasks(TaskSet):
    """Searches for broad category terms to simulate browse-style queries."""

    def on_start(self):
        self.client.get("/", name="GET /homepage")

    @task(2)
    def search_telefon(self):
        do_search(self.client, "telefon")

    @task(2)
    def search_bilgisayar(self):
        do_search(self.client, "bilgisayar")

    @task(1)
    def search_kiyafet(self):
        do_search(self.client, "kıyafet")


class CategorySearchUser(HttpUser):
    tasks = [CategorySearchTasks]
    wait_time = between(2, 4)
    weight = 2


# ── Scenario 3: Empty / edge search ──────────────────────────────────────────

class EdgeSearchTasks(TaskSet):
    """
    Negative / edge scenario: submitting empty or whitespace queries.
    Verifies the server handles these gracefully (no 5xx errors).
    """

    def on_start(self):
        self.client.get("/", name="GET /homepage")

    @task
    def search_empty(self):
        with self.client.get(
            "/arama/",
            params={"q": ""},
            name="/arama/?q=<empty>",
            catch_response=True,
        ) as response:
            # n11.com should respond with 200 or a redirect, not a 5xx
            if response.status_code < 500:
                response.success()
            else:
                response.failure(
                    f"Empty search returned server error: {response.status_code}"
                )

    @task
    def search_whitespace(self):
        with self.client.get(
            "/arama/",
            params={"q": "   "},
            name="/arama/?q=<whitespace>",
            catch_response=True,
        ) as response:
            if response.status_code < 500:
                response.success()
            else:
                response.failure(
                    f"Whitespace search returned server error: {response.status_code}"
                )


class EdgeSearchUser(HttpUser):
    tasks = [EdgeSearchTasks]
    wait_time = between(1, 2)
    weight = 1


# ── Event hooks for summary logging ──────────────────────────────────────────

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats
    print("\n========== Load Test Summary ==========")
    for name, entry in stats.entries.items():
        print(
            f"[{name[1]}] {name[0]}: "
            f"requests={entry.num_requests}, "
            f"failures={entry.num_failures}, "
            f"avg_response={entry.avg_response_time:.0f}ms, "
            f"rps={entry.total_rps:.2f}"
        )
    print("=======================================\n")
