# Setup script for card-detector project
# Run: .\setup.ps1

$PythonPath = "C:\Users\fioravantebossi\AppData\Local\Programs\Python\Python312\python.exe"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Setting up card-detector project..." -ForegroundColor Green

# Create virtual environment
Write-Host "`nCreating virtual environment..."
&$PythonPath -m venv venv

# Activate virtual environment
Write-Host "`nActivating virtual environment..."
&"$ProjectDir\venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "`nInstalling requirements..."
&$PythonPath -m pip install --upgrade pip
&$PythonPath -m pip install -r requirements.txt

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env with your Azure credentials"
Write-Host "2. Run: streamlit run app.py"
