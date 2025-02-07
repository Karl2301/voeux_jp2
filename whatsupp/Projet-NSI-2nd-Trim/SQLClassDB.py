from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(max_length=100, unique=True)
    password_hash: str = Field(max_length=255)
    admin: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    bio: Optional[str] = None
    description: Optional[str] = None
    otp: Optional[int] = None
    session_cookie: Optional[str] = None
    profile_image: Optional[str] = None
    window_location: Optional[str] = None
    banned: bool = Field(default=False)
    admin_level: int = Field(default=0)
    online: bool = Field(default=False)
    two_factor_secret: Optional[str] = None
    verified_email: bool = Field(default=False)
    reason: Optional[str] = None
    dashboard_theme: bool = Field(default=False)

    # Relations
    reports: List["Report"] = Relationship(
        back_populates="reported_user",
        sa_relationship_kwargs={"foreign_keys": "Report.reported_user_id"}
    )
    reported_reports: List["Report"] = Relationship(
        back_populates="reporter_user",
        sa_relationship_kwargs={"foreign_keys": "Report.reporter_user_id"}
    )
    friend_requests_sent: List["FriendRequest"] = Relationship(
        back_populates="requester",
        sa_relationship_kwargs={"foreign_keys": "FriendRequest.requester_id"}
    )
    friend_requests_received: List["FriendRequest"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "FriendRequest.receiver_id"}
    )
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "Conversation.user_id"}
    )
    contacts: List["Contact"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "Contact.user_id"}
    )
    reset_passwords: List["ResetPassword"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "ResetPassword.user_id"}
    )
    images: List["Image"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys": "Image.user_id"}
    )



class Report(SQLModel, table=True):
    __tablename__ = "reports"
    id: Optional[int] = Field(default=None, primary_key=True)
    reported_user_id: str = Field(foreign_key="users.id")
    reporter_user_id: str = Field(foreign_key="users.id")
    reason: Optional[str] = None
    report_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default="pending")

    reported_user: Optional["User"] = Relationship(
        back_populates="reports",
        sa_relationship_kwargs={"foreign_keys": "Report.reported_user_id"}
    )
    reporter_user: Optional["User"] = Relationship(
        back_populates="reported_reports",
        sa_relationship_kwargs={"foreign_keys": "Report.reporter_user_id"}
    )


class FriendRequest(SQLModel, table=True):
    __tablename__ = "friend_requests"
    request_id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: str = Field(foreign_key="users.id")
    receiver_id: str = Field(foreign_key="users.id")
    requester_first_name: str
    requester_last_name: str
    request_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    requester: Optional["User"] = Relationship(
        back_populates="friend_requests_sent",
        sa_relationship_kwargs={"foreign_keys": "FriendRequest.requester_id"}
    )
    receiver: Optional["User"] = Relationship(
        back_populates="friend_requests_received",
        sa_relationship_kwargs={"foreign_keys": "FriendRequest.receiver_id"}
    )


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    contact_id: str = Field(foreign_key="users.id")
    last_message: Optional[str] = None
    type: Optional[str] = None
    publish_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(
        back_populates="conversations",
        sa_relationship_kwargs={"foreign_keys": "Conversation.user_id"}
    )


class Contact(SQLModel, table=True):
    __tablename__ = "contacts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    contact_id: str = Field(foreign_key="users.id")
    last_message: Optional[str] = None
    last_message_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    unread_messages_count: Optional[int] = Field(default=0)

    user: Optional["User"] = Relationship(
        back_populates="contacts",
        sa_relationship_kwargs={"foreign_keys": "Contact.user_id"}
    )


class ResetPassword(SQLModel, table=True):
    __tablename__ = "reset_password"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    token: str = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))

    user: Optional["User"] = Relationship(
        back_populates="reset_passwords",
        sa_relationship_kwargs={"foreign_keys": "ResetPassword.user_id"}
    )


class Image(SQLModel, table=True):
    __tablename__ = "images"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    image_base64: str

    user: Optional["User"] = Relationship(
        back_populates="images",
        sa_relationship_kwargs={"foreign_keys": "Image.user_id"}
    )

