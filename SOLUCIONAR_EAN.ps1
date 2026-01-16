# Script para REINICIAR Odoo y cargar los cambios del módulo
Write-Host "=== SOLUCIONANDO PROBLEMA DE AUTO-POBLACIÓN ===" -ForegroundColor Cyan

Write-Host "`n1. Deteniendo Odoo..." -ForegroundColor Yellow
# Detener todos los procesos de Python que ejecutan Odoo
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw"} | ForEach-Object {
    try {
        $_.Kill()
        Write-Host "   Proceso detenido: $($_.Id)" -ForegroundColor Gray
    } catch {
        Write-Host "   No se pudo detener proceso: $($_.Id)" -ForegroundColor Gray
    }
}

Start-Sleep -Seconds 3

Write-Host "`n2. Iniciando Odoo con código actualizado..." -ForegroundColor Yellow
Write-Host "   Espera a que veas 'HTTP service (werkzeug) running'" -ForegroundColor Cyan
Write-Host ""

# Configurar el PATH
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

# Iniciar Odoo
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\alber\PycharmProjects\odoo19'; .\start_odoo.ps1"

Write-Host "`n✓ Odoo se está iniciando en una nueva ventana" -ForegroundColor Green
Write-Host ""
Write-Host "PASOS FINALES:" -ForegroundColor Yellow
Write-Host "1. Espera a que Odoo termine de iniciar (nueva ventana)" -ForegroundColor White
Write-Host "2. Refresca tu navegador (F5)" -ForegroundColor White
Write-Host "3. Crea un NUEVO pedido de venta" -ForegroundColor White
Write-Host "4. Selecciona Azure Interior como cliente" -ForegroundColor White
Write-Host "5. Agrega cualquier producto" -ForegroundColor White
Write-Host "6. El código EAN aparecerá automáticamente" -ForegroundColor Green
Write-Host ""
