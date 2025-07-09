from hashlib import sha256

mock_users_db = {
    "client@example.com": {
        "password": sha256("client123".encode()).hexdigest(),
        "role": "client"
    },
    "staff@example.com": {
        "password": sha256("staff123".encode()).hexdigest(),
        "role": "staff"
    }
}

def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

def authenticate_user(email: str, password: str) -> bool:
    user = mock_users_db.get(email)
    return user and user["password"] == hash_password(password)

def get_user_role(email: str):
    user = mock_users_db.get(email)
    return user["role"] if user else None
