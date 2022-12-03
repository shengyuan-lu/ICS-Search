from flask import Flask, request, render_template
import re
import json
import os
from nltk.stem import PorterStemmer
import time
import math

app = Flask(__name__)

class Searcher:

    def __init__(self, query):
        self.index_of_index_json = None
        self.sorted_results = None
        self.id_to_url = None

        self.query = query

        final_index_path = os.path.join('Index', 'final_index.txt')
        self.final_index_file = open(final_index_path, 'r')

        tokens = self.tokenize()
        print('Tokenized Query: ' + str(tokens))

        ps = PorterStemmer()

        # parse the index_of_index.json into a python dict
        # and save the result in tokenIndexJson
        self.read_index_of_index()
        self.results = dict()
        self.read_doc_id_dict()

        for token in tokens:
            if len(token)>3:
                stemmed_token = ps.stem(token)
            else:
                stemmed_token = token
            stemmed_token = stemmed_token.lower()

            if stemmed_token in self.index_of_index_json:
                pos = self.index_of_index_json[stemmed_token]
                self.final_index_file.seek(pos)
                json_line = self.final_index_file.readline()

                json_line = json.loads(json_line)
                postings = json_line[stemmed_token]

                df = len(postings)

                for docId in postings:

                    if docId not in self.results:
                        self.results[docId] = dict()
                        self.results[docId]['tokens'] = {token:postings[docId]}
                        self.results[docId]['score'] = 0
                        self.results[docId]['url'] = self.id_to_url[docId]
                        self.results[docId]['missing'] = set(tokens)

                    tf = postings[docId]
                    self.results[docId]['tokens'][token] = postings[docId]
                    self.results[docId]['score'] += self.compute_tfIdf(df, tf)
                    self.results[docId]['missing'] -= {token}

        self.sort_results()
        print(self.sorted_results[0:5])


    def read_index_of_index(self):
        index_of_index = open('index_of_index.json')
        self.index_of_index_json = json.load(index_of_index)
        index_of_index.close()


    def compute_tfIdf(self, df, tf):
        return (1+math.log(tf, 10)) * math.log(self.total_document_count / df, 10)


    def remove_empty(self, lst):
        if "" not in lst:
            return lst
        lst.remove("")
        return self.remove_empty(lst)


    def tokenize(self):

        reg_pattern = '[\s\-\(\)]+'

        reg_token = re.split(reg_pattern, self.query)

        return self.remove_empty(reg_token)


    def read_doc_id_dict(self):
        f = open('doc_id_dict.json')
        self.id_to_url = json.load(f)
        self.total_document_count = len(self.id_to_url)
        f.close()


    def get_results(self, limit = 5):
        result = map(lambda t:t[1], self.sorted_results[0:limit])

        return list(result)


    def sort_results(self):
        self.sorted_results = sorted(self.results.items(), key=lambda t: (len(t[1]['missing']), -t[1]['score']))


@app.route('/search')
def search():
    start_time = time.time()

    query = request.args.get('query')
    query = query.strip()

    if not query:
        query = ''

    print('Original Query: ' + query)

    search_query = Searcher(query)
    results = search_query.get_results(5)
    end_time = time.time()

    return render_template('index.html', results = results, process_time = (end_time-start_time)*1000, query = query)


@app.route('/')
def launch():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)