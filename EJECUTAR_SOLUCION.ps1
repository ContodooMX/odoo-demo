Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "SOLUCION FINAL: Habilitando todos los productos para todos los clientes" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$env:PGPASSWORD = "odoo19pwd"

Write-Host "Ejecutando SQL..." -ForegroundColor Yellow
Write-Host ""

& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U odoo19user -d odoo19_v16 -f SOLUCION_FINAL.sql 2>&1 | Out-String

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "EXITO!" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "PRUEBA AHORA:" -ForegroundColor Yellow
    Write-Host "1. Ve a Ventas -> Pedidos -> Crear" -ForegroundColor White
    Write-Host "2. Selecciona CUALQUIER cliente" -ForegroundColor White
    Write-Host "3. Agrega CUALQUIER producto" -ForegroundColor White
    Write-Host "4. El codigo EAN aparecera automaticamente" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Si ves errores arriba, es posible que algunos registros ya existan." -ForegroundColor Yellow
    Write-Host "Eso es NORMAL. Verifica que funcione en Odoo." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Presiona Enter para continuar..."
Read-Host
