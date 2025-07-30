from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.questions.models import Question, QuestionCreate, QuestionUpdate
from app.questions.services import question_service

router = APIRouter(tags=["questions"])

@router.get("/", response_model=List[Question])
def list_questions():
    try:
        return question_service.get_questions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{question_id}", response_model=Question)
def get_question(question_id: UUID):
    try:
        return question_service.get_question(question_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Question)
def create_question(question: QuestionCreate):
    try:
        return question_service.create_question(question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{question_id}", response_model=Question)
def update_question(question_id: UUID, question: QuestionUpdate):
    try:
        return question_service.update_question(question_id, question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{question_id}")
def delete_question(question_id: UUID):
    try:
        question_service.delete_question(question_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 