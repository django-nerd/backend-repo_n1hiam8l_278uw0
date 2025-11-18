"""
Database Schemas for Coach SaaS

Each Pydantic model represents a collection in your MongoDB database.
Collection name is the lowercase of the class name (e.g., Client -> "client").

These schemas are used for validation and by the integrated database viewer.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
import datetime

# Core domain schemas

class Coach(BaseModel):
    name: str = Field(..., description="Coach full name")
    email: str = Field(..., description="Coach email address")
    company: Optional[str] = Field(None, description="Company or brand name")
    phone: Optional[str] = Field(None, description="Contact phone number")
    plan: str = Field("free", description="Current subscription plan key")
    is_active: bool = Field(True, description="Whether the coach account is active")

class Client(BaseModel):
    coach_id: Optional[str] = Field(None, description="Associated coach ID")
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    goals: Optional[str] = Field(None, description="Client goals or focus areas")
    notes: Optional[str] = Field(None, description="Private notes")
    status: str = Field("active", description="active | paused | archived")

class Session(BaseModel):
    coach_id: Optional[str] = None
    client_id: str = Field(..., description="Linked client id")
    date: datetime.date = Field(..., description="Session date")
    duration_minutes: int = Field(..., ge=0, description="Length in minutes")
    summary: str = Field(..., description="Key outcomes and notes")
    action_items: Optional[List[str]] = Field(default_factory=list, description="Action items for the client")

class Resource(BaseModel):
    coach_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: Optional[str] = Field(None, description="External link if applicable")
    tags: List[str] = Field(default_factory=list)
    visibility: str = Field("private", description="private | shared")

class Contract(BaseModel):
    coach_id: Optional[str] = None
    client_id: Optional[str] = None
    title: str
    body: str = Field(..., description="Contract content (markdown or text)")
    effective_date: Optional[datetime.date] = None
    status: str = Field("draft", description="draft | sent | signed | archived")

class Invoice(BaseModel):
    coach_id: Optional[str] = None
    client_id: Optional[str] = None
    number: str = Field(..., description="Invoice number")
    amount: float = Field(..., ge=0)
    currency: str = Field("USD")
    due_date: Optional[datetime.date] = None
    status: str = Field("unpaid", description="unpaid | paid | void")
    notes: Optional[str] = None

# Public-facing interaction
class ContactMessage(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# Example existing schemas kept for reference (not used by app)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
