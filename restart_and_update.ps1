# Script para reiniciar Odoo y actualizar el módulo sale_customer_code
Write-Host "=== REINICIANDO ODOO Y ACTUALIZANDO MÓDULO ===" -ForegroundColor Cyan

# Configurar el PATH para usar el entorno virtual
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

Write-Host "`n1. Deteniendo cualquier proceso de Odoo..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*odoo-bin*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "`n2. Actualizando módulo sale_customer_code..." -ForegroundColor Yellow
$output = & python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -u sale_customer_code -d odoo19_v16 --stop-after-init 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Módulo actualizado exitosamente!" -ForegroundColor Green
    Write-Host "`n3. Iniciando Odoo..." -ForegroundColor Yellow
    Write-Host "Ejecuta: .\start_odoo.ps1" -ForegroundColor Cyan
} else {
    Write-Host "`n✗ Error al actualizar el módulo" -ForegroundColor Red
    Write-Host "`nÚltimas líneas del error:" -ForegroundColor Yellow
    $output | Select-String -Pattern "Error|Exception|Traceback|ParseError|Field" -Context 2,2 | Select-Object -Last 20
    exit 1
}
