from flask import Flask, request, render_template_string
import webbrowser
from threading import Thread, Event
import time
import logging

app = Flask(__name__)
stop_event = Event()
lines = []
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    try:    
        with open(output_file_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
            f.write(user_input + '\n')
        logger.info("Data saved successfully.")
    except IOError as e:
        logger.error(f"Failed to write to file: {e}")
        return f"Error saving data: {e}"
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

    try:
        with open(input_file_path, 'r') as file:
            lines.extend(line.strip() for line in file.readlines())
    except IOError as e:
        logger.error(f"Failed to read input file: {e}")
        exit(1)

    server_thread = Thread(target=run_server)
    server_thread.start()

    open_browser()

    stop_event.wait()

    print("Flask has been stopped")