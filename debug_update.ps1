$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

Write-Host "Updating sale_customer_code module..." -ForegroundColor Yellow

$output = & python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -u sale_customer_code -d odoo19_v16 --stop-after-init 2>&1

Write-Host "`n=== FULL OUTPUT ===" -ForegroundColor Cyan
$output | ForEach-Object { Write-Host $_ }

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nModule updated successfully!" -ForegroundColor Green
} else {
    Write-Host "`nModule update failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "`n=== ERRORS ===" -ForegroundColor Red
    $output | Select-String -Pattern "ERROR|Error|error|Exception|Traceback" | ForEach-Object { Write-Host $_ -ForegroundColor Red }
}
