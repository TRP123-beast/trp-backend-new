import os
from supabase import create_client, Client
from app.user.models import User, UserCreate, UserUpdate
from typing import List, Optional
from uuid import UUID
from passlib.context import CryptContext

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase URL or Key not set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def get_users() -> List[User]:
        data, count, error = supabase.table("users").select("*").execute()
        if error:
            raise Exception(error.message)
        return [User(**item) for item in data]

    @staticmethod
    def get_user(user_id: UUID) -> Optional[User]:
        data, count, error = supabase.table("users").select("*").eq("id", str(user_id)).single().execute()
        if error:
            raise Exception(error.message)
        return User(**data)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        data, count, error = supabase.table("users").select("*").eq("email", email).single().execute()
        if error:
            return None
        return User(**data)

    @staticmethod
    def create_user(user: UserCreate) -> User:
        # Hash the password
        hashed_password = UserService.get_password_hash(user.password)
        user_data = user.dict()
        user_data.pop("password")
        user_data["password_hash"] = hashed_password
        
        data, count, error = supabase.table("users").insert(user_data).execute()
        if error:
            raise Exception(error.message)
        return User(**data[0])

    @staticmethod
    def update_user(user_id: UUID, user: UserUpdate) -> User:
        data, count, error = supabase.table("users").update(user.dict(exclude_unset=True)).eq("id", str(user_id)).execute()
        if error:
            raise Exception(error.message)
        return User(**data[0])

    @staticmethod
    def delete_user(user_id: UUID):
        data, count, error = supabase.table("users").delete().eq("id", str(user_id)).execute()
        if error:
            raise Exception(error.message)
        return True

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_email(email)
        if not user:
            return None
        if not UserService.verify_password(password, user.password_hash):
            return None
        return user

user_service = UserService() 