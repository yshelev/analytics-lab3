# Analytics lab 2

Создан пайплайн, который из файла data/input.csv, содержащего отзывы о фильмах,
выбирает текст одного случайного отзыва, анализирует на эмоциональность с помощью LLM, и записывает ответ в output.json

# Входные данные
см. data/input.csv

# Выходные данные 
см. data/output.json

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
4. Заполнить .env по примеру .env.example и положить его в корень проекта 
5. Настроить виртуальное окружение 
```sh
python -m venv .venv 
.venv/Scripts/activate
```
6. Установить зависимости командой 
```sh
pip install -r requirements.txt
```
7. Запустить проект командой 
```sh
python main.py 
```