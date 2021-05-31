@echo off
CD = %CD%/bin
set /p var=¦w¸Ë Python3.9.5? (Y/N):
if "%var%" == "y" (
	echo Install Python
	%CD%/python-3.9.5-amd64.exe
)else if "%var%" == "Y" (
	echo Install Python
	python-3.9.5-amd64.exe /quiet
)
python --version
python -m pip install selenium
python -m pip install pywin32
python -m pip install pypiwin32
python -m pip install requests
python -m pip install Pillow
python %CD%/chrome_helper.py
echo Install Complete
pause