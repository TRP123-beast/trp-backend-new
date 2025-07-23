import os
from supabase import create_client, Client
from schemas.flag import Flag, FlagCreate, FlagUpdate
from typing import List, Optional
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase URL or Key not set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class FlagService:
    @staticmethod
    def get_flags() -> List[Flag]:
        res = supabase.table("flags").select("*").execute()
        if res.error:
            raise Exception(res.error.message)
        return [Flag(**item) for item in res.data]

    @staticmethod
    def get_flag(flag_id: UUID) -> Optional[Flag]:
        res = supabase.table("flags").select("*").eq("id", str(flag_id)).single().execute()
        if res.error:
            raise Exception(res.error.message)
        return Flag(**res.data)

    @staticmethod
    def create_flag(flag: FlagCreate) -> Flag:
        res = supabase.table("flags").insert(flag.dict()).execute()
        if res.error:
            raise Exception(res.error.message)
        return Flag(**res.data[0])

    @staticmethod
    def update_flag(flag_id: UUID, flag: FlagUpdate) -> Flag:
        res = supabase.table("flags").update(flag.dict(exclude_unset=True)).eq("id", str(flag_id)).execute()
        if res.error:
            raise Exception(res.error.message)
        return Flag(**res.data[0])

    @staticmethod
    def delete_flag(flag_id: UUID):
        res = supabase.table("flags").delete().eq("id", str(flag_id)).execute()
        if res.error:
            raise Exception(res.error.message)
        return True

flag_service = FlagService() 