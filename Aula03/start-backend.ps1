Write-Host "=== Backend ===" -ForegroundColor Green
Write-Host "Instalando dependências..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt

Write-Host "`nIniciando o servidor FastAPI..." -ForegroundColor Yellow
Write-Host "Acesse: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentação: http://localhost:8000/docs" -ForegroundColor Cyan
uvicorn main:app --reload --host 0.0.0.0 --port 8000
