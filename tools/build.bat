@echo off

:: The path to the build folder
SET "build_path=build"
:: 7zip CLI path
SET "seven_zip=C:\Program Files\7-Zip"

:: The repo and dependencies
SET repo_path=%~dp0..
SET "bluik_path=%repo_path%\bluik"
SET "dublf_path=%repo_path%\..\DuBLF\dublf"
SET "oco_path=%repo_path%\..\..\OCO\ocopy"

echo Building: %repo_path%
echo To: %build_path%

:: remove previous version
for /r "%build_path%" /d %%a IN (*) do IF /i "%%~nxa"=="bluik" rd /s /q "%%a"
rd "%build_path%\bluik"

:: copy main files
echo Copying: "%bluik_path%\"
md "%build_path%\bluik"
for /f %%a IN ('dir /b "%bluik_path%\*.py"') do copy "%bluik_path%\%%a" "%build_path%\bluik\%%a"

:: copy dublf
echo Copying: "%dublf_path%\"
md "%build_path%\bluik\dublf"
for /f %%a IN ('dir /b "%dublf_path%\*.py"') do copy "%dublf_path%\%%a" "%build_path%\bluik\dublf\%%a"

:: copy oco
echo Copying: "%oco_path%\"
md "%build_path%\bluik\ocopy"
for /f %%a IN ('dir /b "%oco_path%\*.py"') do copy "%oco_path%\%%a" "%build_path%\bluik\ocopy\%%a"

:: zip
del "%build_path%\bluik.zip"
"%seven_zip%\7z.exe" a "%build_path%\bluik.zip" ".\%build_path%\*"
