# Analytics lab 3

бот, который получает сначала датасет в формате excel/csv, затем по этому датасету выполняет запросы пользователя 

# start
Для старта необходимо: 

1. Склонировать репозиторий 
```sh
git clone https://github.com/yshelev/analytics_lab3.git
```
2. Перейти в директорию проекта
```sh
cd analytics_lab3
```
3. Получить api key для ллм на сайте https://console.groq.com/ 
4. Получить api key для бота у @BotFather
5. Заполнить .env по примеру .env.example и положить его в корень проекта 
6. Настроить виртуальное окружение 
```sh
python -m venv .venv 
.venv/Scripts/activate
```
7. Установить зависимости командой 
```sh
pip install -r requirements.txt
```
8. Запустить проект командой 
```sh
python main.py 
```