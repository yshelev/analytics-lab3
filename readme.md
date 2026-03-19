# Analytics lab 3

бот, который получает огромный текст и отправляет в ллм запрос с просьбой выделить самое важное из этого текста, и выводит ответ пользователю

# start
Для старта необходимо: 

1. Склонировать репозиторий 
```sh
git clone https://github.com/yshelev/analytics_lab2.git
```
2. Перейти в директорию проекта
```sh
cd analytics_lab2
```
3. Получить api key на сайте https://openrouter.ai/ 
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