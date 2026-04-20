@echo off
set DATE=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE=%DATE: =0%
mysqldump -u root -p delivery_system_v2026 > backup_%DATE%.sql
echo Backup completed: backup_%DATE%.sql
pause2