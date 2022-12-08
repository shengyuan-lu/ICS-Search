from flask import Flask, request, render_template
import time
from Searcher import Searcher

app = Flask(__name__)

@app.route('/search')
def search():
    start_time = time.time()
    query = request.args.get('query')
    query = query.strip()

    if not query:
        query = ''

    print('Original Query: ' + query)

    search_query = Searcher(query)
    results = search_query.get_results(10)
    end_time = time.time()

    return render_template('index.html', results = results, process_time = (end_time-start_time)*1000, query = query)


@app.route('/')
def launch():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)