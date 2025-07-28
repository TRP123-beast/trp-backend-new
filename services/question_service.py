import os
from supabase import create_client, Client
from schemas.question import Question, QuestionCreate, QuestionUpdate
from typing import List, Optional
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase URL or Key not set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class QuestionService:
    @staticmethod
    def get_questions() -> List[Question]:
        data, count, error = supabase.table("questions").select("*").execute()
        if error:
            raise Exception(error.message)
        return [Question(**item) for item in data]

    @staticmethod
    def get_question(question_id: UUID) -> Optional[Question]:
        data, count, error = supabase.table("questions").select("*").eq("id", str(question_id)).single().execute()
        if error:
            raise Exception(error.message)
        return Question(**data)

    @staticmethod
    def create_question(question: QuestionCreate) -> Question:
        data, count, error = supabase.table("questions").insert(question.dict()).execute()
        if error:
            raise Exception(error.message)
        return Question(**data[0])

    @staticmethod
    def update_question(question_id: UUID, question: QuestionUpdate) -> Question:
        data, count, error = supabase.table("questions").update(question.dict(exclude_unset=True)).eq("id", str(question_id)).execute()
        if error:
            raise Exception(error.message)
        return Question(**data[0])

    @staticmethod
    def delete_question(question_id: UUID):
        data, count, error = supabase.table("questions").delete().eq("id", str(question_id)).execute()
        if error:
            raise Exception(error.message)
        return True

question_service = QuestionService() 