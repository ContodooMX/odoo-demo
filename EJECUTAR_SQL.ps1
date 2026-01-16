# Script para ejecutar SQL y habilitar todos los productos para todos los clientes
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES" -ForegroundColor Green
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

# Ejecutar SQL usando psql
Write-Host "Ejecutando script SQL..." -ForegroundColor Yellow

$env:PGPASSWORD = "admin"
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U odoo -d odoo19_v16 -f enable_all_products.sql

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "="*80 -ForegroundColor Green
    Write-Host "COMPLETADO!" -ForegroundColor Green  
    Write-Host "="*80 -ForegroundColor Green
    Write-Host ""
    Write-Host "Todos los productos ahora están disponibles para todos los clientes." -ForegroundColor White
    Write-Host ""
    Write-Host "PRUEBA:" -ForegroundColor Yellow
    Write-Host "1. Ve a Ventas -> Pedidos -> Crear" -ForegroundColor White
    Write-Host "2. Selecciona CUALQUIER cliente" -ForegroundColor White
    Write-Host "3. Agrega CUALQUIER producto" -ForegroundColor White
    Write-Host "4. El código EAN aparecerá automáticamente" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Error al ejecutar SQL" -ForegroundColor Red
    Write-Host ""
}
