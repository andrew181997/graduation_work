from dataclasses import dataclass, field
from typing import List, Dict, Any


# @dataclass
# class UserData:
#     """Датакласс для описания сущности пользователя"""
#     editByOwnerOnly: int
#     login: str
#     fullName: str
#     userRoles: List[str]
#     phone: str
#     newPassword: str
#     additionalEmails: List[str]
#     address: Dict[str, Any]  # Любые поля
#     preferences: Dict[str, Any]  # Любые поля внутри
#     contracts: List[Any]
#     parties: List[Any]
#     confirmPassword: str

@dataclass
class UserData:
    """
    Датакласс с описанием сущности пользователя
    """
    entity_id: int = None # id
    owner_id: int = None # id контрагента
    owner_name: str = None # название контрагента
    full_name: str = "AUTOTEST_USER" # полное имя
    login: str = "auto_data@test.ru" # логин
    job: str = None # должность
    roles: list[str] = field(default_factory=list) # Список ролей пользователя
    passwd: str = "1q2w3e" # пароль пользователя
    notifications: list[str] = field(default_factory=list) #Нотификации
    contracts: list[str] = field(default_factory=list) # контракты пользователя
    parties: str = None # контрагенты пользователя
    allowed_ip: str = False # доступные ip
    ips: list[str] = field(default_factory=list[str]) # заблокированные ip
    has_startup_popup: bool = False # включен ли у пользователя визард