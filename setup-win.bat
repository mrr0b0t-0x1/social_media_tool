@echo OFF
:: This is a setup file for Social Media Tool
:: It installs all the pre-requisistes and set the environment
::===============================================================

title Social Media Tool - Setup

echo.
echo =================================================
echo Social Media Tool - Setup
echo =================================================
echo.

:: Set working directory
rem cd %USERPROFILE%\Desktop\social_media_tool
cd %~dp0

::===============================================================

:: Check if all the pre-requisites are installed

:: Check if Python is installed
for /f "delims=" %%i in ('where python 2^>nul') do set PYLOC=%%i

if defined PYLOC (
	goto :PYTHONFOUND
) else (
	echo ERROR: Python is not installed
	goto :SETTITLE
)
:: Check Python version
:PYTHONFOUND
for /f "delims=" %%i in ('%PYLOC% --version') do set PYVER=%%i
echo %PYVER% | findstr /C:"Python 3.6" 1>nul

if %ERRORLEVEL% equ 0 (
	echo Required Python version found: %PYVER%
) else (
	:: Check alternate paths where Python 3.6 may be installed
	if exist %USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe ( 
		set PYLOC=%USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe
		for /f "delims=" %%i in ('%PYLOC% --version') do set PYVER=%%i
        echo %PYVER% | findstr /C:"Python 3.6" 1>nul

        if %ERRORLEVEL% equ 0 (
            echo Required Python version found: %PYVER%
        ) else (
            echo Some error occurred while checking Python version
            goto :SETTITLE
        )
	) else ( 
		echo ERROR: Please make sure Python 3.6 is installed
		goto :SETTITLE
	)
)
echo.

:: Check if Node is installed
for /f "delims=" %%i in ('where node 2^>nul') do set NODELOC="%%i" & goto :NODEPATH
:NODEPATH
if defined NODELOC (
	goto :NODEFOUND
) else (
	echo ERROR: Node is not installed
	goto :SETTITLE
)
:: Check Node version
:NODEFOUND
for /f "delims=" %%i in ('%NODELOC% -v') do set NODEVER=%%i
echo %NODEVER% | findstr /C:"v15." 1>nul

if %ERRORLEVEL% equ 0 (
	echo Required Node version found: %NODEVER%
) else (
	echo ERROR: Please make sure Node version 15+ is installed
	goto :SETTITLE
)
echo.
:: Check if NPM is installed
for /f "delims=" %%i in ('where npm 2^>nul') do set NPMLOC="%%i" & goto :NPMPATH
:NPMPATH
if defined NPMLOC (
	goto :NPMFOUND
) else (
	echo ERROR: NPM is not installed
	goto :SETTITLE
)
:: Check NPM version
:NPMFOUND
for /f "delims=" %%i in ('%NPMLOC% -v') do set NPMVER=%%i
echo %NPMVER% | findstr /C:"v7." 1>nul

if %ERRORLEVEL% equ 0 (
	echo Required NPM version found: %NPMVER%
) else (
	echo ERROR: Please make sure NPM version 7+ is installed
	goto :SETTITLE
)
echo.

:: Check if Git is installed
::for /f "delims=" %%i in ('where git 2^>nul') do set GITLOC=%%i

::if defined GITLOC (
::	echo Git is installed
::) else (
::	echo ERROR: Git is not installed
::	goto :SETTITLE
::)
::echo.

::===============================================================

:: Make Python venv for project
echo Creating venv and activating...
cmd /C "%PYLOC% -m venv venv1 & venv1\Scripts\activate"
echo.

:: Updating pip
echo Updating pip...
cmd /C "venv1\Scripts\python.exe -m pip install --upgrade --no-cache-dir pip"
echo.

:: Install setuptools
echo Installing setuptools...
cmd /C "venv1\Scripts\python.exe -m pip install --upgrade --no-cache-dir --force-reinstall setuptools"
echo.

:: Install python modules
echo Installing required Python modules...
cmd /C "venv1\Scripts\python.exe -m pip install --upgrade --force-reinstall --exists-action i -r requirements.txt"
echo.

:: Install npm modules
echo Installing required Node modules...
cmd /C "cd ui & npm install"

::===============================================================

:SETTITLE
title Social Media Tool - Setup
echo.

PAUSE