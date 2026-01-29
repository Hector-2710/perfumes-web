from typing import Any, Dict, Optional

class EssenciaRabeException(Exception):
    """Base exception for EssenciaRabe project"""
    def __init__(self, message: str, status_code: int = 400, headers: Optional[Dict[str, str]] = None):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        super().__init__(self.message)

# --- Entity Exceptions ---

class EntityNotFoundError(EssenciaRabeException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(message=f"{entity_name} with identity '{entity_id}' not found", status_code=404)

class UserNotFoundError(EntityNotFoundError):
    def __init__(self, user_id: Any):
        super().__init__("User", user_id)

class ProductNotFoundError(EntityNotFoundError):
    def __init__(self, product_id: Any):
        super().__init__("Product", product_id)

# --- Auth Exceptions ---

class AuthenticationError(EssenciaRabeException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(
            message=message,
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedError(EssenciaRabeException):
    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message=message, status_code=403)

# --- Business Logic Exceptions ---

class DuplicateEntityError(EssenciaRabeException):
    def __init__(self, entity_name: str, field: str, value: Any):
        super().__init__(
            message=f"{entity_name} with {field} '{value}' already exists",
            status_code=409
        )

class OutOfStockError(EssenciaRabeException):
    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(
            message=f"Insufficient stock for '{product_name}'. Requested: {requested}, Available: {available}",
            status_code=400
        )

class InvalidOrderStateError(EssenciaRabeException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)
