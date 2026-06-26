@echo off
echo ================================================
echo  Generando PDF e enviando newsletter de cobertura
echo ================================================
cd /d "C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal"
py newsletter_cobertura.py
echo.
if %errorlevel%==0 (
    echo [OK] Proceso completado correctamente.
) else (
    echo [ERROR] Algo ha fallado. Revisa los mensajes anteriores.
)
echo.
pause
