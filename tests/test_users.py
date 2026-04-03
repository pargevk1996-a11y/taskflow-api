from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserUpdate


def test_get_and_update_user(db):
    auth_service = AuthService(db)
    auth_service.register(
        RegisterRequest(
            email="user1@example.com",
            login="user1",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    user_service = UserService(db)
    user = user_service.get_user(1)
    assert user.email == "user1@example.com"

    updated = user_service.update_user(1, UserUpdate(login="user1_updated"))
    assert updated.login == "user1_updated"
