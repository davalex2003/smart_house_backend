from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    @task(2)
    def index(self):
        self.register()
        self.get_devices()

    def register(self):
        payload = {
            "name": "Алексей",
            "surname": "Давиденко",
            "e_mail": "davalex2003@yandex.ru",
            "hash_password": "password"
        }
        self.client.post("/users/register", json=payload)

    def get_devices(self):
        headers = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlX21haWwiOiJkYXZhbGV4MjAwM0B5YW5kZXgucnUiLCJoYXNoX3Bhc3N3b3JkIjoicGFzc3dvcmQifQ.nEgwbEYPq-Yifavqx0tirJeUcGBp8ysmuxGXcmFVbRk"
        }
        self.client.get("/devices/get_all", headers=headers)

    def on_stop(self):
        self.delete()

    def delete(self):
        headers = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlX21haWwiOiJkYXZhbGV4MjAwM0B5YW5kZXgucnUiLCJoYXNoX3Bhc3N3b3JkIjoicGFzc3dvcmQifQ.nEgwbEYPq-Yifavqx0tirJeUcGBp8ysmuxGXcmFVbRk"
        }
        self.client.delete("/users/delete", headers=headers)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000
