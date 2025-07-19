from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, validator
from datetime import datetime

from app.database import get_db
from app.models import Todo

router = APIRouter()

# Pydantic 모델 정의
class TodoCreate(BaseModel):
    title: str
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('할 일을 입력해주세요.')
        if len(v.strip()) > 200:
            raise ValueError('할 일은 200자 이내로 입력해주세요.')
        return v.strip()

class TodoUpdate(BaseModel):
    title: str | None = None
    status: bool | None = None
    
    @validator('title')
    def title_validation(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('할 일을 입력해주세요.')
            if len(v.strip()) > 200:
                raise ValueError('할 일은 200자 이내로 입력해주세요.')
            return v.strip()
        return v

class TodoResponse(BaseModel):
    id: int
    title: str
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 모든 Todo 조회
@router.get("", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todo).order_by(Todo.created_at.desc()).all()
        return todos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="데이터베이스 오류가 발생했습니다.")

# 새 Todo 생성
@router.post("", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = Todo(title=todo.title)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="할 일 추가 중 오류가 발생했습니다.")

# Todo 업데이트
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    try:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="해당 할 일을 찾을 수 없습니다.")
        
        if todo.title is not None:
            db_todo.title = todo.title
        if todo.status is not None:
            db_todo.status = todo.status
        
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="업데이트 중 오류가 발생했습니다.")

# Todo 삭제
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="해당 할 일을 찾을 수 없습니다.")
        
        db.delete(db_todo)
        db.commit()
        return {"detail": "할 일이 삭제되었습니다."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="삭제 중 오류가 발생했습니다.")