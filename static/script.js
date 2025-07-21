// API 기본 URL - 현재 경로 기반으로 설정
const BASE_PATH = window.location.pathname.replace(/\/$/, '');
const API_URL = `${BASE_PATH}/api/todos`;

// DOM 요소
const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');

// 페이지 로드 시 Todo 목록 불러오기
document.addEventListener('DOMContentLoaded', loadTodos);

// 이벤트 리스너
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

// HTML 이스케이프 함수 (XSS 방지)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 에러 메시지 표시 함수
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #f44336;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(errorDiv);
    
    // 3초 후 자동 제거
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => errorDiv.remove(), 300);
    }, 3000);
}

// Todo 목록 불러오기
async function loadTodos() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('서버 응답 오류');
        }
        const todos = await response.json();
        displayTodos(todos);
    } catch (error) {
        console.error('Todo 목록을 불러오는 중 오류 발생:', error);
        showError('할 일 목록을 불러올 수 없습니다. 잠시 후 다시 시도해주세요.');
    }
}

// Todo 목록 표시
function displayTodos(todos) {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = createTodoElement(todo);
        todoList.appendChild(li);
    });
}

// Todo 요소 생성
function createTodoElement(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.status ? 'completed' : ''}`;
    li.dataset.id = todo.id;
    
    li.innerHTML = `
        <input 
            type="checkbox" 
            class="todo-checkbox" 
            ${todo.status ? 'checked' : ''}
            onchange="toggleTodo(${todo.id}, this.checked)"
        >
        <span class="todo-text" onclick="toggleTodo(${todo.id}, ${!todo.status})">${escapeHtml(todo.title)}</span>
        <button class="delete-btn" onclick="deleteTodo(${todo.id})">삭제</button>
    `;
    
    return li;
}

// 새 Todo 추가
async function addTodo() {
    const title = todoInput.value.trim();
    
    // 입력 검증
    if (!title) {
        showError('할 일을 입력해주세요.');
        todoInput.focus();
        return;
    }
    
    if (title.length > 200) {
        showError('할 일은 200자 이내로 입력해주세요.');
        return;
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '서버 오류');
        }
        
        todoInput.value = '';
        await loadTodos();
    } catch (error) {
        console.error('Todo 추가 중 오류 발생:', error);
        showError('할 일 추가에 실패했습니다. 다시 시도해주세요.');
    }
}

// Todo 상태 토글
async function toggleTodo(id, status) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status }),
        });
        
        if (!response.ok) {
            throw new Error('상태 변경 실패');
        }
        
        await loadTodos();
    } catch (error) {
        console.error('Todo 상태 변경 중 오류 발생:', error);
        showError('상태 변경에 실패했습니다.');
    }
}

// Todo 삭제
async function deleteTodo(id) {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error('삭제 실패');
        }
        
        await loadTodos();
    } catch (error) {
        console.error('Todo 삭제 중 오류 발생:', error);
        showError('삭제에 실패했습니다.');
    }
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);