# SOLUCIÓN FINAL - EJECUTA ESTE SCRIPT

Write-Host "=== SOLUCIÓN DEFINITIVA CÓDIGO EAN ===" -ForegroundColor Green
Write-Host ""

# Configurar PATH
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

Write-Host "PASO 1: Deteniendo Odoo..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "✓ Odoo detenido" -ForegroundColor Green

Write-Host "`nPASO 2: Iniciando Odoo..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\alber\PycharmProjects\odoo19'; python odoo\odoo-bin -c odoo.conf --addons-path 'odoo\addons,enterprise,addons' -d odoo19_v16"

Write-Host "✓ Odoo iniciándose en nueva ventana" -ForegroundColor Green

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "AHORA SIGUE ESTOS PASOS:" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""
Write-Host "1. ESPERA 30 segundos a que Odoo inicie completamente" -ForegroundColor White
Write-Host "   (verás 'HTTP service (werkzeug) running' en la otra ventana)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Ve a tu navegador y REFRESCA (F5)" -ForegroundColor White
Write-Host ""
Write-Host "3. Crea un NUEVO pedido de venta" -ForegroundColor White
Write-Host ""
Write-Host "4. Selecciona 'Azure Interior' como cliente" -ForegroundColor White
Write-Host ""
Write-Host "5. Agrega el producto '[E-COM11] Cabinet with Doors'" -ForegroundColor White
Write-Host ""
Write-Host "6. El código 'GABINETE1003' DEBE aparecer automáticamente" -ForegroundColor Green
Write-Host ""
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Si NO aparece el código, mira los LOGS en la otra ventana" -ForegroundColor Red
Write-Host "Busca líneas que digan '=== ONCHANGE PRODUCT TRIGGERED ==='" -ForegroundColor Red
Write-Host ""
