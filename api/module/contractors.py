import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ContractorData:
    editByOwnerOnly: int = 0
    name: str = f"test_party_{uuid.uuid4().hex[:8]}"
    partyRoles: List[str] = field(default_factory=lambda: ["SERVICE_SUPPLIER", "CUSTOMER"])
    status: str = "ACTIVE"
    addressDto: Dict[str, Any] = field(default_factory=dict)
    users: List[Dict[str, Any]] = field(default_factory=list)
    slaSupplier: int = 0
    serviceSupplier: int = 0
    customer: int = 0
    active: int = 0
    autoPublishReport: int = 1
    hasRestrictions: int = 0
    roles: Dict[str, int] = field(default_factory=lambda: {"slaSupplier": 1, "serviceSupplier": 1, "customer": 1})
    partyReport: Dict[str, Any] = field(default_factory=dict)
    phone: str = ""
