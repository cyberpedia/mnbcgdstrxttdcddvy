from datetime import UTC, datetime, timedelta

from locust import HttpUser, between, task


class CerberusUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.username = f"load_{int(datetime.now(UTC).timestamp()*1000)}"
        self.password = "VeryStrongPassword123!"
        self.client.post(
            "/auth/register",
            json={
                "username": self.username,
                "email": f"{self.username}@load.local",
                "password": self.password,
                "role": "admin",
            },
        )
        login = self.client.post(
            "/auth/login",
            json={"username": self.username, "password": self.password},
        ).json()
        self.headers = {
            "Authorization": f"Bearer {login['access_token']}",
            "X-CSRF-Token": login["csrf_token"],
            "X-User-Id": "1",
        }

        event = self.client.post(
            "/events",
            headers=self.headers,
            json={
                "name": f"LoadEvent-{self.username}",
                "start_time": datetime.now(UTC).isoformat(),
                "end_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
                "status": "live",
            },
        ).json()
        self.event_id = event["id"]
        challenge = self.client.post(
            "/challenges",
            headers=self.headers,
            json={
                "event_id": self.event_id,
                "title": "Load Challenge",
                "category": "web",
                "difficulty": "easy",
                "type": "standard",
                "hierarchical_rule": {},
                "visibility": "public",
            },
        ).json()
        self.challenge_id = challenge["id"]
        self.client.post(
            f"/challenges/{self.challenge_id}/sub-challenges",
            headers=self.headers,
            json={"title": "Part A", "order": 1, "flag": "flag{ok}"},
        )

    @task(3)
    def leaderboard_read(self):
        self.client.get(f"/leaderboard/{self.event_id}", headers=self.headers)

    @task(2)
    def challenge_submit(self):
        self.client.post(
            "/leaderboard/submit",
            headers=self.headers,
            params={"event_id": self.event_id, "challenge_id": self.challenge_id, "flag": "flag{ok}"},
        )

    @task(1)
    def notifications_send(self):
        self.client.post(
            "/notifications/ws-send",
            headers=self.headers,
            json={"user_id": 1, "type": "load", "content": "load test ping"},
        )
