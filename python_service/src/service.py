"""
Sample Target Service - Codeme Examples
A domain-driven user registration service demonstrating quality and invariant compliance.
"""
from typing import Dict, Any, Optional

class User:
    def __init__(self, user_id: str, email: str, status: str = "active"):
        self.user_id = user_id
        self.email = email
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "status": self.status
        }

class UserService:
    def __init__(self):
        self._users: Dict[str, User] = {}

    def register_user(self, user_id: str, email: str) -> User:
        if "@" not in email:
            raise ValueError("Invalid email format")
        user = User(user_id=user_id, email=email)
        self._users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
