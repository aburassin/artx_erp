
from frappe.auth import LoginManager

def authenticate_user(user_id: str, pwd: str) -> None:
    """
    Authenticate the user with the given user ID and password.

    Args:
        user_id (str): User ID
        pwd (str): Password

    Returns:
        None: Raises AuthenticationError if authentication fails
    """
    login_manager = LoginManager()
    login_manager.authenticate(user=user_id, pwd=pwd)
    login_manager.post_login()