from flask import Flask, render_template, request
import csv
import plotly.graph_objs as go



app = Flask(__name__)

# Загрузка стартовой страницы
@app.route('/')
def index():
    return render_template('index.html')

# Обработка загрузки файла
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file.filename == '':
        return 'Ошибка: файл не выбран'

    if file and file.filename.endswith('.csv'):
        try:
            # Чтение файла CSV
            reader = csv.DictReader(file)
            data = list(reader)

            # Фильтрация данных
            filtered_data = [row for row in data if row['Actress'] == 'Bardot Brigitte' and row['Category'] == 'Actress']

            if not filtered_data:
                return render_template('index.html', message='Нет данных для отображения')

            # Создание графика
            x = [row['Year'] for row in filtered_data]
            y = [row['Title'] for row in filtered_data]
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
            fig.update_layout(title='Фильмы с участием Bardot Brigitte', xaxis_title='Year', yaxis_title='Title')

            return render_template('index.html', plot=fig.to_html(), message='Файл успешно загружен и обработан')

        except csv.Error:
            return render_template('index.html', message='Ошибка при чтении файла CSV')

    return render_template('index.html', message='Ошибка: неверный формат файла')

if __name__ == '__main__':
    app.run(debug=True)
