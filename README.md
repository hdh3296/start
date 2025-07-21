# Todo 애플리케이션

FastAPI와 PostgreSQL을 사용한 간단한 Todo 애플리케이션입니다.

## 기술 스택

- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 15
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Container**: Docker & Docker Compose
- **Deployment**: DigitalOcean App Platform

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
│   └── api/
│       └── todos.py     # Todo API 라우트
├── static/
│   ├── script.js        # 프론트엔드 JavaScript (동적 API 경로 포함)
│   └── style.css        # CSS 스타일
├── templates/
│   └── index.html       # HTML 템플릿
├── main.py              # FastAPI 앱 진입점 (root_path 설정 포함)
├── requirements.txt     # Python 패키지
├── Dockerfile          # Docker 이미지 빌드 설정
├── docker-compose.yml  # Docker 컴포즈 설정
├── nginx-todo-config.conf # Nginx 리버스 프록시 설정
├── check-server-status.sh # 서버 상태 확인 스크립트
└── deployment-checklist.md # 배포 체크리스트

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
http://localhost:8001
```

### 개발 모드

코드 변경 시 자동으로 재시작됩니다 (volume 마운팅 설정).

### 데이터베이스 접속

PostgreSQL 컨테이너 직접 접속:
```bash
docker exec -it todo-postgres psql -U todouser -d tododb
```

### 리버스 프록시 배포

URL prefix로 배포할 경우 (예: /todo/):

1. 환경변수 설정:
```yaml
environment:
  - ROOT_PATH=/todo
```

2. Nginx 설정:
```nginx
location /todo/ {
    proxy_pass http://127.0.0.1:8001/;
    proxy_set_header Host $host;
    # ... 기타 프록시 헤더
}
```

## API 엔드포인트

- `GET /api/todos` - 모든 Todo 조회
- `POST /api/todos` - 새 Todo 생성
- `PUT /api/todos/{todo_id}` - Todo 상태 업데이트
- `DELETE /api/todos/{todo_id}` - Todo 삭제
- `GET /health` - 헬스 체크

## 환경 설정

### 데이터베이스 설정

환경 변수로 데이터베이스 URL 설정 가능:
- `DATABASE_URL`: PostgreSQL 연결 URL (기본값: SQLite)
- `ROOT_PATH`: URL prefix 설정 (기본값: /todo) - 리버스 프록시 배포 시 사용

### PostgreSQL 설정

개발 환경:
- Database: tododb
- User: todouser
- Password: todopass
- Port: 5432 (로컬), 5433 (Docker 호스트)

### 프로덕션 환경

DigitalOcean Droplet에 Docker로 배포:
- URL: http://174.138.30.39/todo/
- 포트: 8001 (Docker) → 80 (Nginx)
- 데이터베이스: PostgreSQL 15 (Docker 컨테이너)

## 보안 고려사항

- XSS 방지를 위한 입력 검증 및 HTML 이스케이프
- SQL Injection 방지 (SQLAlchemy ORM 사용)
- 에러 메시지 최소화
- CORS 설정으로 Cross-Origin 요청 제어
- 입력 길이 제한 (200자)

## 배포

### DigitalOcean Droplet (현재)
이 애플리케이션은 DigitalOcean Droplet에 Docker로 배포되어 있습니다:
- URL: http://174.138.30.39/todo/
- 웹 서버: Nginx (리버스 프록시)
- 컨테이너: Docker & Docker Compose
- 데이터베이스: PostgreSQL 15 (Docker 컨테이너)

#### 배포 구조
- Blog Batgan 앱: http://174.138.30.39/ (포트 8000)
- Todo 앱: http://174.138.30.39/todo/ (포트 8001)
- Nginx가 경로 기반으로 라우팅

### DigitalOcean App Platform (이전)
- URL: https://adam-app-gu4lz.ondigitalocean.app/
- 자동 배포: GitHub master 브랜치 푸시 시 자동 배포
- 데이터베이스: PostgreSQL 17 (관리형 데이터베이스)

## 마이그레이션 히스토리

- 2025-01-21: DigitalOcean Droplet Docker 배포
  - URL prefix (/todo/) 지원을 위한 FastAPI root_path 설정
  - 정적 파일 경로 동적 변환 구현
  - JavaScript API 경로 동적 설정
  - Nginx 리버스 프록시 설정 추가
  - blog-batgan 앱과 공존하도록 포트 설정 (8001, 5433)
  
- 2025-01-19: MySQL에서 PostgreSQL로 데이터베이스 마이그레이션
  - Python 3.13에서 3.12로 다운그레이드 (psycopg3 호환성)
  - pymysql에서 psycopg[binary]로 드라이버 변경
  - API 엔드포인트 trailing slash 제거 (307 리다이렉트 방지)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.