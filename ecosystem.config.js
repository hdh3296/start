module.exports = {
  apps: [{
    name: 'todo-app',
    script: '/var/www/todo-app/venv/bin/uvicorn',
    args: 'main:app --host 0.0.0.0 --port 8001',
    cwd: '/var/www/todo-app',
    env: {
      DATABASE_URL: 'postgresql://todouser:todopass@localhost:5432/tododb'
    }
  }]
};