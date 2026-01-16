# Script para revertir el módulo al estado original
Write-Host "=== REVIRTIENDO MÓDULO AL ESTADO ORIGINAL ===" -ForegroundColor Cyan

$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

Write-Host "`nActualizando módulo a versión original..." -ForegroundColor Yellow
$output = & python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -u sale_customer_code -d odoo19_v16 --stop-after-init 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Módulo revertido exitosamente!" -ForegroundColor Green
    Write-Host "`nEl módulo está de vuelta a su estado original." -ForegroundColor Green
    Write-Host "Ahora puedes iniciar Odoo con: .\start_odoo.ps1" -ForegroundColor Cyan
} else {
    Write-Host "`n✗ Error al revertir el módulo" -ForegroundColor Red
    Write-Host "`nDetalles del error:" -ForegroundColor Yellow
    $output | Select-String -Pattern "Error|Exception|Traceback" -Context 1,1 | Select-Object -Last 15
    exit 1
}
