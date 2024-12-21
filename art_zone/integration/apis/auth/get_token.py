
import frappe
from .generate_keys import generate_keys
from .authenticate_user import authenticate_user
from frappe import _
def get_user_token(user , password):
    
    try:
        user_id = get_user_id(user)
        if not user_id:
            raise frappe.AuthenticationError
        authenticate_user(user_id, password)
        user = frappe.get_doc("User", user)
        access_token = generate_keys(user.name)
        response = {
            "status": "success",
            "message": "User authenticated successfully",
            "access_token": access_token
        }
        frappe.local.response["message"] = response

    except frappe.AuthenticationError:
        set_error_response(_("AuthenticationError"), _("Invalid username, email, or password"))
    except Exception as e:
        set_error_response(_("Error"), f"An unexpected error occurred: {str(e)}")






def get_user_id(usr: str) -> str:
    """
    Get the user ID based on the username or email.

    Args:
        usr (str): Username or Email

    Returns:
        str: User ID if found, else None
    """
    user = frappe.db.get_value("User", {"username": usr}) or frappe.db.get_value("User", {"email": usr})
    return user

def set_error_response(status: str, message: str) -> None:
    """
    Set an error response.

    Args:
        status (str): Status of the error
        message (str): Error message

    Returns:
        None: Response is set in frappe.local.response
    """
    frappe.local.response["message"] = {
        "status": status,
        "message": message,
    }