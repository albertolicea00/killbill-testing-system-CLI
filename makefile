build-windows-64:
	pip install --upgrade pip
	pip install pyinstaller
	pyinstaller --name win-script_64 --onefile main.py

build-windows-32:
	pip install --upgrade pip
	pip install pyinstaller
	pyinstaller --name win-script_32 --onefile --distpath dist_32 main.py
