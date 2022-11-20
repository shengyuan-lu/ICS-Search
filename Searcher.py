# GOAL For Search

# Your program should prompt the user for a query.
# This doesn’t need to be a Web interface, it can be a console prompt.
# At the time of the query, your program will stem the query terms, look up your index, perform some calculations (see ranking below) and give out the ranked list of pages that are relevant for the query, with the most relevant on top.
# Pages should be identified by their URLs.

# Ranking: at the very least, your ranking formula should include tf-idf scoring, and take the important words into consideration, but you should feel free to add additional components to this formula if you think they improve the retrieval.

# IMPORT OTHER CLASSES HERE
from flask import Flask, jsonify, request, render_template
import re
import json
import os
from nltk.stem import PorterStemmer

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
            stemmed_token = ps.stem(token)

            if stemmed_token in self.index_of_index_json:
                pos = self.index_of_index_json[stemmed_token]
                self.final_index_file.seek(pos)
                json_line = self.final_index_file.readline()

                json_line = json.loads(json_line)
                postings = json_line[stemmed_token]
                new_dict = dict()

                # if the result dictionary is empty
                if not bool(self.results):
                    for docId in postings:

                        new_dict[docId] = {token:postings[docId]}
                        new_dict[docId]['url'] = self.id_to_url[docId]
                        new_dict[docId]['score'] = postings[docId]
                    self.results = new_dict
                # if not empty
                else:
                    for docId in postings:
                        #docId = self.idToUrl[docId]
                        if docId in self.results:

                            new_dict[docId] = self.results[docId]
                            new_dict[docId]['url'] = self.id_to_url[docId]
                            new_dict[docId][token] = postings[docId]
                            new_dict[docId]['score'] += postings[docId]

                    self.results = new_dict

        self.sort_results()

    def read_index_of_index(self):
        index_of_index = open('index_of_index.json')
        self.index_of_index_json = json.load(index_of_index)
        index_of_index.close()


    def tokenize(self):
        pattern = '\s+'
        return re.split(pattern,self.query)


    def read_doc_id_dict(self):
        f = open('doc_id_dict.json')
        self.id_to_url = json.load(f)
        f.close()


    def get_results(self, limit = 5):
        result = map(lambda t:t[1]['url'], self.sorted_results[0:limit])

        return list(result)


    def sort_results(self):
        self.sorted_results = sorted(self.results.items(), key=lambda t: -t[1]['score'])


@app.route('/search')
def search():
    query = request.args.get('query')
    query = query.strip()

    if not query:
        query = ''

    print('Original Query: ' + query)

    search_query = Searcher(query)
    results = search_query.get_results()

    return render_template('index.html', results = results)


@app.route('/')
def launch():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)