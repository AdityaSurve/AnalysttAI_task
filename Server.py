from flask import Flask, request, send_file, render_template_string
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        return "<div><h1>API is working</h1></div>"

    data = get_data()

    table_html = generate_table_html(data)

    with open('index.html', 'r') as file:
        template_string = file.read()

    template_string = template_string.replace('{{ table_html }}', table_html)

    return render_template_string(template_string)

def get_data():
    with open('amazon.csv', 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data

def generate_table_html(data):
    table_header = "<tr><th>Title</th><th>Rating</th><th>Link</th><th>Price(₹)</th><th>Number of Reviews</th></tr>"
    table_rows = ""

    for row in data[1:]:
        row_html = "<tr>"
        for value in row:
            row_html += f"<td>{value}</td>"
        row_html += "</tr>"
        table_rows += row_html

    table_html = f"""
    <table class="table">
        {table_header}
        {table_rows}
    </table>
    """
    return table_html

if __name__ == '__main__':
    app.run()
