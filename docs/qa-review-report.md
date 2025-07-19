# Todo 앱 QA 리뷰 보고서

## 🎯 개요
- **프로젝트**: Todo 앱 (FastAPI + HTML/CSS/JS + SQLite)
- **리뷰어**: Quinn (Senior Developer & QA Architect)
- **날짜**: 2025-01-19

## 🚨 즉시 수정이 필요한 사항 (Critical)

### 1. XSS 취약점 수정
**문제**: JavaScript에서 todo.title을 직접 HTML에 삽입하여 XSS 공격 가능
```javascript
// 현재 코드 (취약함)
<span class="todo-text">${todo.title}</span>
```

**해결책**:
```javascript
// 안전한 코드
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 사용
<span class="todo-text">${escapeHtml(todo.title)}</span>
```

### 2. 입력 검증 강화
**문제**: 백엔드에서 입력 검증 부족

**해결책** - Pydantic 모델 개선:
```python
from pydantic import BaseModel, validator

class TodoCreate(BaseModel):
    title: str
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must be less than 200 characters')
        return v.strip()
```

## ⚠️ 중요 개선사항 (High Priority)

### 1. 에러 핸들링 개선
**백엔드**:
```python
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = Todo(title=todo.title)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
```

**프론트엔드**:
```javascript
async function addTodo() {
    const title = todoInput.value.trim();
    if (!title) {
        showError('할 일을 입력해주세요');
        return;
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            showError(error.detail || '오류가 발생했습니다');
            return;
        }
        
        todoInput.value = '';
        await loadTodos();
    } catch (error) {
        showError('서버 연결에 실패했습니다');
    }
}

function showError(message) {
    // 에러 메시지 표시 UI 구현
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    // ...
}
```

### 2. 코드 구조 개선
**JavaScript 모듈화**:
```javascript
const TodoApp = (function() {
    const API_URL = '/api/todos';
    let todos = [];
    
    function init() {
        bindEvents();
        loadTodos();
    }
    
    function bindEvents() {
        document.getElementById('addBtn').addEventListener('click', addTodo);
        // ...
    }
    
    // private methods...
    
    return { init };
})();

document.addEventListener('DOMContentLoaded', TodoApp.init);
```

### 3. 환경 설정 개선
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./todos.db"
    cors_origins: list = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 📋 테스트 계획

### 1. 단위 테스트 (pytest)
```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/api/todos", json={"title": "Test Todo"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_create_todo_empty_title():
    response = client.post("/api/todos", json={"title": ""})
    assert response.status_code == 422
```

### 2. 프론트엔드 테스트 (Jest)
```javascript
// todo.test.js
describe('Todo App', () => {
    test('should escape HTML in todo titles', () => {
        const maliciousTitle = '<script>alert("XSS")</script>';
        const escaped = escapeHtml(maliciousTitle);
        expect(escaped).not.toContain('<script>');
    });
});
```

## 🎯 성능 최적화 제안

1. **디바운싱 추가**: 빠른 입력 시 API 호출 제한
2. **가상 스크롤**: Todo 항목이 많을 때 성능 향상
3. **로컬 상태 관리**: 낙관적 업데이트로 UX 개선

## 📊 코드 품질 메트릭

- **보안 점수**: 6/10 (XSS 취약점으로 감점)
- **유지보수성**: 7/10 (구조는 깔끔하나 모듈화 필요)
- **테스트 가능성**: 8/10 (의존성 주입 잘됨)
- **성능**: 7/10 (기본적인 최적화 필요)

## 🚀 다음 단계

1. **즉시**: XSS 취약점 수정 및 입력 검증 추가
2. **단기**: 에러 핸들링 개선 및 테스트 추가
3. **중기**: 코드 구조 개선 및 성능 최적화

---

**결론**: 학습용 프로젝트로는 훌륭하지만, 프로덕션 사용을 위해서는 보안과 에러 핸들링 개선이 필수적입니다.