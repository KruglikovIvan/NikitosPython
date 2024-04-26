import webbrowser
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

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
    <form method="POST">
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
    shutdown_server() # Завершение работы фласка
    return 'Data saved. Server shutting down.'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    input_file_path = 'input.txt' # Путь к файлу с данными для формы
    output_file_path = 'output.txt' # Путь к файлу с данными из формы

    with open(input_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()