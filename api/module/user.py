import uuid
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
    editByOwnerOnly: bool = False
    login: str = field(default_factory=lambda: f"test_user_{uuid.uuid4().hex[:8]}@example.com")
    fullName: str = "AUTOTEST_USER1"  # полное имя
    userRoles: List[str] = field(default_factory=lambda: ["SIMPLE_USER"])
    phone: str = field(default_factory=str)
    newPassword: str = "0000"
    confirmPassword: str = "0000"
    additionalEmails: list[str] = field(default_factory=list)
    address: dict[str] = field(default_factory=lambda:{"country":"","postcode":"","city":"","street":"","house":"","floor":"","room":""})
    preferences: Dict[str, Any] = field(
        default_factory=lambda: {
            "isAllowedIps": 0,
            "troubleTicketsPopup": 1,
            "slaReportsPublishPopup": 0,
            "welcomeMessagePopup": 0,
            "actionEventPopup": 0,
            "useScale": 1,
            "ips": [""],
            "notificationSubscriptions": [],
            "mobileNotificationSubscriptions": ["TT_LEVEL_NODATA","TT_LEVEL_FAILURE","TT_CLOSE","TT_OPEN","TT_LEVEL_DEGRADATION"],
            "notificationChannels": [],
            "baseUrl": ""
        }
    )
    contracts: list[str] = field(default_factory=list)
    parties: list[str] = field(default_factory=list) # контрагенты пользователя
    # entity_id: int = None # id
    # owner_id: int = None # id контрагента
    # owner_name: str = None # название контрагента
    # full_name: str = "AUTOTEST_USER" # полное имя
    #
    # job: str = None # должность
    # passwd: str = "1q2w3e" # пароль пользователя
    # notifications: list[str] = field(default_factory=list) #Нотификации
    # contracts: list[str] = field(default_factory=list) # контракты пользователя
    # parties: str = None # контрагенты пользователя
    # allowed_ip: str = False # доступные ip
    # ips: list[str] = field(default_factory=list[str]) # заблокированные ip
    # has_startup_popup: bool = False # включен ли у пользователя визард