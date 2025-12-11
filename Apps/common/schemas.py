from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLog(BaseModel):
    """Schema para un registro de auditoría"""
    id_log: int
    user_id: int
    action: str
    details: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AuditLogWithUser(BaseModel):
    """Schema para log de auditoría con información del usuario"""
    id_log: int
    user_id: int
    user_name: str
    user_email: str
    action: str
    details: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
