# Script para habilitar todos los productos para todos los clientes
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES" -ForegroundColor Green
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

# Configurar PATH
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

Write-Host "Ejecutando script..." -ForegroundColor Yellow
Write-Host ""

python enable_all_products_all_customers.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "="*80 -ForegroundColor Green
    Write-Host "✓ ÉXITO!" -ForegroundColor Green
    Write-Host "="*80 -ForegroundColor Green
    Write-Host ""
    Write-Host "Todos los clientes ahora tienen acceso a todos los productos" -ForegroundColor White
    Write-Host "con sus códigos EAN configurados." -ForegroundColor White
    Write-Host ""
    Write-Host "PRUEBA:" -ForegroundColor Yellow
    Write-Host "1. Ve a Ventas → Pedidos → Crear" -ForegroundColor White
    Write-Host "2. Selecciona CUALQUIER cliente" -ForegroundColor White
    Write-Host "3. Agrega CUALQUIER producto" -ForegroundColor White
    Write-Host "4. El código EAN aparecerá automáticamente" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Error al ejecutar el script" -ForegroundColor Red
    Write-Host "Revisa los mensajes de error arriba" -ForegroundColor Yellow
    Write-Host ""
}
