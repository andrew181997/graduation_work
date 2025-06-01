from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class UserData:
    """Датакласс для описания сущности пользователя"""
    editByOwnerOnly: int
    login: str
    fullName: str
    userRoles: List[str]
    phone: str
    newPassword: str
    additionalEmails: List[str]
    address: Dict[str, Any]  # Любые поля
    preferences: Dict[str, Any]  # Любые поля внутри
    contracts: List[Any]
    parties: List[Any]
    confirmPassword: str