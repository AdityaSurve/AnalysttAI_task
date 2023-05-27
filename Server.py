from flask import Flask, request
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        return "<div><h1>API is working</h1></div>"
    
    data = get_data()  # Replace this with your data source
    
    table_html = generate_table_html(data)
    return f"<div><h1>API is working</h1>{table_html}</div>"

def get_data():
    # Replace this function with your own logic to fetch the data
    # For demonstration purposes, we're reading data from a CSV file
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

    table_html = f"<table>{table_header}{table_rows}</table>"
    return table_html

if __name__ == '__main__':
    app.run()
