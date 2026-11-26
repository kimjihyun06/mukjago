@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo  먹자GO - 자료\엑셀 전체 사진/상세페이지 연결
echo ============================================
git pull
echo.
echo [1/4] 미리보기 (아직 아무것도 바뀌지 않음)
python tools\import_all_photos.py --dry
if errorlevel 1 goto end
echo.
set OK=
set /p OK=  위처럼 연결할까요? (y/N) 
if /i not "%OK%"=="y" goto end
echo.
echo [2/4] 연결 + 홈페이지 갱신
python tools\import_all_photos.py
echo.
echo [3/4] 점검
python tools\state.py check
if errorlevel 1 (echo  점검에서 문제가 있어 올리지 않습니다. & goto end)
echo.
set UP=
set /p UP=  [4/4] 홈페이지에 올릴까요(배포)? (y/N) 
if /i not "%UP%"=="y" goto end
git add -A
git commit -m "자료 폴더 사진·상세페이지 전체 연결"
git push
echo  올렸습니다. 1~2분 뒤 https://kimjihyun06.github.io/mukjago/ 에 반영됩니다.
:end
pause
