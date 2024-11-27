@echo off

:: The path to Blender
SET "blender_config_path=%appData%\Blender Foundation\Blender\4.3"

:: The repo and dependencies
SET repo_path=%~dp0..
SET "bluik_path=%repo_path%\bluik"
SET "dublf_path=%repo_path%\..\DuBLF\dublf"
SET "oco_path=%repo_path%\..\..\OCO\ocopy"

:: Need admin to create symlinks
@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
:: Get back to original dir
pushd "%CD%"
CD /D "%~dp0"

:: get/create scripts path
md "%blender_config_path%\scripts"
md "%blender_config_path%\scripts\addons"
SET "addons_path=%blender_config_path%\scripts\addons"

:: remove previous version
for /r "%addons_path%" /d %%a IN (*) do IF /i "%%~nxa"=="bluik" rd /s /q "%%a"
rd "%addons_path%\bluik"

:: create folder
md "%addons_path%\bluik"

:: link main files
for /f %%a IN ('dir /b "%bluik_path%\*.py"') do mklink "%addons_path%\bluik\%%a" "%bluik_path%\%%a"

:: link dublf
md "%addons_path%\bluik\dublf"
for /f %%a IN ('dir /b "%dublf_path%\*.py"') do mklink "%addons_path%\bluik\dublf\%%a" "%dublf_path%\%%a"
:: link oco
mklink /D "%addons_path%\bluik\ocopy" "%oco_path%"

pause