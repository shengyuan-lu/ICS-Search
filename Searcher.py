import re
import json
import os
from nltk.stem import PorterStemmer
import math

class Searcher:

    def __init__(self, query):
        self.index_of_index_json = None
        self.sorted_results = None
        self.id_to_url = None

        self.query = query
        self.file_path = os.path.dirname(os.path.abspath(__name__))
        print(self.file_path)
        final_index_path = os.path.join(self.file_path,'Index', 'final_index.txt')

        with open(final_index_path, 'r') as file:
            self.final_index_file = file

        tokens = self.tokenize()
        print('Tokenized Query: ' + str(tokens))

        ps = PorterStemmer()

        # parse the index_of_index.json into a python dict
        # and save the result in tokenIndexJson
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
        complete_path = os.path.join(self.file_path,'index_of_index.json')
        with open(complete_path, 'r') as index_of_index:
            self.index_of_index_json = json.load(index_of_index)


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
        complete_path = os.path.join(self.file_path,'doc_id_dict.json')

        with open(complete_path, 'r') as file:
            self.id_to_url = json.load(file)
            self.total_document_count = len(self.id_to_url)


    def get_results(self, limit = 5,page=1):
        
        result = map(lambda t:t[1], self.sorted_results[((page-1)*limit):((page-1)*limit+limit)])

        return list(result)


    def sort_results(self):
        self.sorted_results = sorted(self.results.items(), key=lambda t: (len(t[1]['missing']), -t[1]['score']))
        self.total = len(self.sorted_results)


    def get_total(self):
        return self.total
