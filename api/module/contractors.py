from dataclasses import dataclass, field


@dataclass
class ContractorData:
    """
    Датакласс для описания сущности контрагента
    """
    id: int = None #id
    owner_id: int = None #id владельца
    owner_name: str = None # имя владельца
    edit_by_owner: bool = False # блокировка редактирования
    name: str = "auto_contractor_default_name" # название
    users: field(default_factory=list) = None # список пользователей
    parent_party_ids: field(default_factory=list[int]) = None # материнские id
    parent_party_names: field(default_factory=list[str]) = None # материнские названия
    party_roles: field(default_factory=list[str]) = None  # роли ["CUSTOMER"]
    phone: str = None #телефон
    address_dto: field(default_factory=dict) = None #адрес
    sla_supplier: bool = False # является провайдером SLA?
    service_supplier: bool = False # является провайдером сервиса?
    customer: bool = False # является потребителем?

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ContractorData:
    tags: List[str] = field(default_factory=list)
    customFields: List[str] = field(default_factory=list)
    editByOwnerOnly: int = 0
    name: str = "test_python111111"
    partyRoles: List[str] = field(default_factory=lambda: ["SLA_SUPPLIER", "SERVICE_SUPPLIER", "CUSTOMER"])
    status: str = "ACTIVE"
    addressDto: Dict[str, Any] = field(default_factory=dict)
    users: List[str] = field(default_factory=list)
    slaSupplier: int = 0
    serviceSupplier: int = 0
    customer: int = 0
    active: int = 0
    autoPublishReport: int = 1
    hasRestrictions: int = 0
    roles: Dict[str, int] = field(default_factory=lambda: {"slaSupplier": 1, "serviceSupplier": 1, "customer": 1})
    partyReport: Dict[str, Any] = field(default_factory=dict)
    phone: str = ""