import httpx
import uuid
import random
import string
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000"
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
TEST_EMAIL = f"testuser_{random_suffix}@example.com"
TEST_PASSWORD = "StrongPassword123!"

def test_auth():
    print(f"--- Starting tests for user: {TEST_EMAIL} ---")
    client = httpx.Client(base_url=BASE_URL)

    # 1. Register
    print("\n1. Testing POST /api/auth/register")
    register_payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": "Test User",
        "birth_date": "1990-01-01",
        "onboarding_answers": {
            "pregunta_guia": "amor",
            "estilo_lectura": "directa",
            "vision_destino": "destino_fijo"
        }
    }
    res = client.post("/api/auth/register", json=register_payload)
    print(f"Status: {res.status_code}")
    pprint(res.json())
    if res.status_code != 200:
        print("Register failed!")
        return

    # 2. Login
    print("\n2. Testing POST /api/auth/login")
    login_payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    res = client.post("/api/auth/login", json=login_payload)
    print(f"Status: {res.status_code}")
    pprint(res.json())
    if res.status_code != 200:
        print("Login failed!")
        return
    
    auth_data = res.json()
    access_token = auth_data["access_token"]
    refresh_token = auth_data["refresh_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 3. Get /me
    print("\n3. Testing GET /api/auth/me")
    res = client.get("/api/auth/me", headers=headers)
    print(f"Status: {res.status_code}")
    pprint(res.json())

    # 4. Put /profile
    print("\n4. Testing PUT /api/auth/profile")
    profile_payload = {
        "preferred_language": "en"
    }
    res = client.put("/api/auth/profile", json=profile_payload, headers=headers)
    print(f"Status: {res.status_code}")
    pprint(res.json())

    # 5. Post /refresh
    print("\n5. Testing POST /api/auth/refresh")
    refresh_payload = {
        "refresh_token": refresh_token
    }
    res = client.post("/api/auth/refresh", json=refresh_payload)
    print(f"Status: {res.status_code}")
    pprint(res.json())

    # 6. Post /logout
    print("\n6. Testing POST /api/auth/logout")
    res = client.post("/api/auth/logout", headers=headers)
    print(f"Status: {res.status_code}")
    pprint(res.json())

if __name__ == "__main__":
    test_auth()
