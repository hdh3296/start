# Todo 애플리케이션

FastAPI와 MySQL을 사용한 간단한 Todo 애플리케이션입니다.

## 기술 스택

- **Backend**: FastAPI (Python 3.13)
- **Database**: MySQL 8.0
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Container**: Docker & Docker Compose

## 주요 기능

- ✅ Todo 항목 추가
- ✅ Todo 항목 삭제
- ✅ Todo 상태 토글 (완료/미완료)
- ✅ 완료된 항목 스타일링 (회색 + 취소선)
- ✅ 실시간 UI 업데이트

## 프로젝트 구조

```
.
├── app/
│   ├── __init__.py
│   ├── database.py      # 데이터베이스 연결 설정
│   ├── models.py        # SQLAlchemy 모델
│   └── routes.py        # API 라우트
├── static/
│   ├── script.js        # 프론트엔드 JavaScript
│   └── style.css        # CSS 스타일
├── templates/
│   └── index.html       # HTML 템플릿
├── main.py              # FastAPI 앱 진입점
├── requirements.txt     # Python 패키지
├── Dockerfile          # Docker 이미지 빌드 설정
├── docker-compose.yml  # Docker 컴포즈 설정
└── .dockerignore       # Docker 빌드 제외 파일

```

## 시작하기

### 사전 요구사항

- Docker
- Docker Compose

### 설치 및 실행

1. 프로젝트 클론
```bash
git clone [repository-url]
cd start
```

2. Docker Compose로 실행
```bash
docker-compose up --build
```

3. 브라우저에서 접속
```
http://localhost:8000
```

### 개발 모드

코드 변경 시 자동으로 재시작됩니다 (volume 마운팅 설정).

### 데이터베이스 접속

MySQL 컨테이너 직접 접속:
```bash
docker exec -it todo-mysql mysql -u todouser -ptodopass tododb
```

## API 엔드포인트

- `GET /api/todos/` - 모든 Todo 조회
- `POST /api/todos/` - 새 Todo 생성
- `PUT /api/todos/{todo_id}` - Todo 상태 업데이트
- `DELETE /api/todos/{todo_id}` - Todo 삭제

## 환경 설정

### 데이터베이스 설정

환경 변수로 데이터베이스 URL 설정 가능:
- `DATABASE_URL`: MySQL 연결 URL (기본값: SQLite)

### MySQL 설정

- Database: tododb
- User: todouser
- Password: todopass
- Port: 3306
- Character Set: utf8mb4

## 보안 고려사항

- XSS 방지를 위한 입력 검증
- SQL Injection 방지 (SQLAlchemy ORM 사용)
- 에러 메시지 최소화

## 알려진 이슈

- MySQL에서 한글 문자가 제대로 저장되지 않는 문제가 있음 (수정 중)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.