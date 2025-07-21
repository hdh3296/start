# DigitalOcean Droplet 배포 체크리스트

## 방화벽 설정
```bash
# UFW 방화벽 설정
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 환경 변수 보안
- `.env` 파일은 절대 Git에 포함하지 마세요
- 프로덕션 환경에서는 강력한 데이터베이스 비밀번호 사용
- `DATABASE_URL`에 실제 비밀번호 설정

## 데이터베이스 보안
```bash
# PostgreSQL 외부 접속 차단 (로컬만 허용)
sudo nano /etc/postgresql/*/main/postgresql.conf
# listen_addresses = 'localhost'

sudo systemctl restart postgresql
```

## 정기 백업
```bash
# 데이터베이스 백업 스크립트
pg_dump -U todouser tododb > /backup/tododb_$(date +%Y%m%d).sql
```

## 모니터링
- PM2 웹 모니터링: `pm2 web`
- 시스템 리소스: `htop`
- Nginx 액세스 로그: `/var/log/nginx/access.log`