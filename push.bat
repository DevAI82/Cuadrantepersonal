@echo off
cd /d "C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal"
if exist .git\index.lock del .git\index.lock
if exist .git\HEAD.lock del .git\HEAD.lock
git add index.html
git commit -m "actualizacion cuadrante"
git push
pause
