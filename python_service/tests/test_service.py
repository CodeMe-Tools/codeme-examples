import pytest
from src.service import UserService

def test_register_and_get_user():
    service = UserService()
    user = service.register_user("usr_123", "alice@example.com")
    assert user.user_id == "usr_123"
    assert user.email == "alice@example.com"
    assert service.get_user("usr_123") == user

def test_invalid_email_raises():
    service = UserService()
    with pytest.raises(ValueError):
        service.register_user("usr_456", "not-an-email")
