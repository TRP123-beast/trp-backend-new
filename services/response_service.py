import os
from supabase import create_client, Client
from schemas.response import Response, ResponseCreate, ResponseUpdate
from typing import List, Optional
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase URL or Key not set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ResponseService:
    @staticmethod
    def get_responses() -> List[Response]:
        res = supabase.table("responses").select("*").execute()
        if res.error:
            raise Exception(res.error.message)
        return [Response(**item) for item in res.data]

    @staticmethod
    def get_response(response_id: UUID) -> Optional[Response]:
        res = supabase.table("responses").select("*").eq("id", str(response_id)).single().execute()
        if res.error:
            raise Exception(res.error.message)
        return Response(**res.data)

    @staticmethod
    def create_response(response: ResponseCreate) -> Response:
        res = supabase.table("responses").insert(response.dict()).execute()
        if res.error:
            raise Exception(res.error.message)
        return Response(**res.data[0])

    @staticmethod
    def update_response(response_id: UUID, response: ResponseUpdate) -> Response:
        res = supabase.table("responses").update(response.dict(exclude_unset=True)).eq("id", str(response_id)).execute()
        if res.error:
            raise Exception(res.error.message)
        return Response(**res.data[0])

    @staticmethod
    def delete_response(response_id: UUID):
        res = supabase.table("responses").delete().eq("id", str(response_id)).execute()
        if res.error:
            raise Exception(res.error.message)
        return True

response_service = ResponseService() 