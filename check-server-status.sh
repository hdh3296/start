#!/bin/bash

echo "=== DigitalOcean Droplet 서버 상태 확인 ==="
echo "서버 IP: 174.138.30.39"
echo "========================================="

echo -e "\n[1] 시스템 정보"
uname -a
lsb_release -a 2>/dev/null || cat /etc/os-release

echo -e "\n[2] 시스템 리소스"
echo "--- 디스크 사용량 ---"
df -h

echo -e "\n--- 메모리 사용량 ---"
free -m

echo -e "\n--- CPU 정보 ---"
nproc
uptime

echo -e "\n[3] 실행 중인 웹 서비스"
echo "--- PM2 프로세스 ---"
pm2 list 2>/dev/null || echo "PM2가 설치되지 않았습니다"

echo -e "\n--- 사용 중인 포트 ---"
sudo netstat -tlnp | grep LISTEN | grep -E ':(80|443|3000|5000|8000|8001|8080|5432|3306)'

echo -e "\n[4] Nginx 설정"
echo "--- 활성화된 사이트 ---"
ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "Nginx가 설치되지 않았습니다"

echo -e "\n--- Nginx 상태 ---"
sudo systemctl status nginx --no-pager 2>/dev/null | head -10

echo -e "\n[5] 프로젝트 디렉토리"
echo "--- /var/www ---"
ls -la /var/www/ 2>/dev/null

echo "--- /home ---"
ls -la /home/*/

echo -e "\n[6] 데이터베이스"
echo "--- PostgreSQL 데이터베이스 목록 ---"
sudo -u postgres psql -l 2>/dev/null || echo "PostgreSQL이 설치되지 않았습니다"

echo -e "\n--- MySQL 데이터베이스 목록 ---"
mysql -u root -e "SHOW DATABASES;" 2>/dev/null || echo "MySQL이 설치되지 않았습니다"

echo -e "\n[7] 환경 변수 및 설정 파일"
echo "--- 환경 변수 파일 ---"
ls -la /home/*/.env 2>/dev/null
ls -la /var/www/*/.env 2>/dev/null

echo -e "\n========================================="
echo "서버 상태 확인 완료"