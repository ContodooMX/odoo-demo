# Script para actualizar el modulo sale_customer_code y reiniciar Odoo
# Este script detiene Odoo, actualiza el modulo, y lo reinicia

Write-Host "Actualizando modulo sale_customer_code..." -ForegroundColor Yellow

# Configurar el PATH para usar el entorno virtual
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

# Actualizar el modulo
Write-Host "Ejecutando actualizacion del modulo..." -ForegroundColor Cyan
python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -u sale_customer_code -d odoo19_v16 --stop-after-init

if ($LASTEXITCODE -eq 0) {
    Write-Host "Modulo actualizado exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ahora puedes iniciar Odoo con:" -ForegroundColor Yellow
    Write-Host "  .\start_odoo.ps1" -ForegroundColor Cyan
} else {
    Write-Host "Error al actualizar el modulo" -ForegroundColor Red
    exit 1
}
