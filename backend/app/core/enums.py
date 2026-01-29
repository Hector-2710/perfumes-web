from enum import Enum

class ProductType(str, Enum):
    SEALED = "sealed"
    DECANT = "decant"
    NONE = "none"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"