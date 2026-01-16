# Script para reiniciar Odoo limpiamente
# Detiene cualquier proceso de Odoo y lo reinicia

Write-Host "Deteniendo procesos de Odoo..." -ForegroundColor Yellow

# Buscar y detener todos los procesos de Python relacionados con Odoo
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*odoo19*"} | Stop-Process -Force

Write-Host "Esperando 3 segundos..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host "Iniciando Odoo..." -ForegroundColor Green
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH
python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -d odoo19_v16
