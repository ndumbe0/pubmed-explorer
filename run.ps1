param(
  [string]$mode = "dev"
)

if ($mode -eq "dev") {
  Write-Host "Starting PubMed Explorer in dev mode..."
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload --port 8003"
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
}
