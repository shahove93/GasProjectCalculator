CWD: D:\Antigravity\GasProjectCalculator
DATE: 2026-11-11
SOURCE: README.md (UTF-8), selected line ranges
---- Installer section (lines 8-17) ----
8: Для обычного пользователя готовый установщик уже собран локально: **Python и
9: командная строка не нужны**.
10: 
11: 1. Откройте установщик:
12:    `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`
13:    (размер 15 256 037 байт, SHA256
14:    `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`).
15: 2. Запустите его и пройдите мастер установки. Установка выполняется только для
16:    текущего пользователя, в каталог
17:    `%LOCALAPPDATA%\Programs\GasProjectCalculator`; права администратора не

COMMAND: Select-String -Path README.md -Pattern '2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F','GasProjectCalculator-Setup-1.0.0.exe','uvicorn','unittest discover'
12:    `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`
14:    `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`).
146: .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
160: .\.venv\Scripts\python.exe -m unittest discover -s tests
177: .\.venv\Scripts\python.exe -m uvicorn app.main:app

---- Developer section (lines 138-182) ----
138: ```powershell
139: python -m venv .venv
140: .\.venv\Scripts\python.exe -m pip install -r requirements.txt
141: ```
142: 
143: ### Запуск сервера
144: 
145: ```powershell
146: .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
147: ```
148: 
149: ### Где открыть приложение
150: 
151: После запуска сервера откройте в браузере:
152: 
153: ```
154: http://127.0.0.1:8000/
155: ```
156: 
157: ### Тесты
158: 
159: ```powershell
160: .\.venv\Scripts\python.exe -m unittest discover -s tests
161: ```
162: 
163: ### Запуск из исходного кода на другом компьютере
164: 
165: Эта инструкция — только для запуска из исходного кода. Обычному пользователю
166: нужен установщик из раздела «Установка на Windows».
167: 
168: 1. Установите Python 3.10 или новее с сайта [python.org](https://www.python.org/downloads/windows/).
169:    В установщике включите **Add Python to PATH**.
170: 2. На [странице ветки feature/gsv в GitHub](https://github.com/shahove93/GasProjectCalculator/tree/feature/gsv)
171:    нажмите **Code → Download ZIP**, затем распакуйте архив.
172: 3. Откройте PowerShell в распакованной папке проекта и выполните:
173: 
174: ```powershell
175: python -m venv .venv
176: .\.venv\Scripts\python.exe -m pip install -r requirements.txt
177: .\.venv\Scripts\python.exe -m uvicorn app.main:app
178: ```
179: 
180: 4. Откройте <http://127.0.0.1:8000/> в браузере. Чтобы остановить сервер,
181:    нажмите `Ctrl+C` в PowerShell.
182: 
