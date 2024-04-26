from flask import Flask, request, render_template_string
import webbrowser
from threading import Thread, Event
import time

app = Flask(__name__)

stop_event = Event()
lines = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Форма пользователя</title>
</head>
<body>
    <h1>Данные из файла</h1>
    <ul>
        {% for line in lines %}
        <li>{{ line }}</li>
        {% endfor %}
    </ul>
    <h2>Ввод данных пользователем</h2>
    <form method="POST" onsubmit="try { window.close(); } catch(e) { console.log('Browser preventing closing'); }">
        <input type="text" name="user_input" required>
        <button type="submit">OK</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def form():
    return render_template_string(HTML_TEMPLATE, lines=lines)

@app.route('/', methods=['POST'])
def form_post():
    user_input = request.form['user_input']
    with open(output_file_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
        f.write(user_input + '\n')
    stop_event.set() # Остановка фласка
    return 'Data saved. Server shutting down.'

def run_server():
    app.run(debug=False, use_reloader=False)

def open_browser():
    time.sleep(1)
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    input_file_path = 'input.txt' # Путь к файлу с данными для формы
    output_file_path = 'output.txt' # Путь к файлу с данными из формы

    with open(input_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    server_thread = Thread(target=run_server)
    server_thread.start()

    open_browser()

    stop_event.wait()

    print("Flask has been stopped")