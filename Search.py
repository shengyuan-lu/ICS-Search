# GOAL For Search

# Your program should prompt the user for a query.
# This doesn’t need to be a Web interface, it can be a console prompt.
# At the time of the query, your program will stem the query terms, look up your index, perform some calculations (see ranking below) and give out the ranked list of pages that are relevant for the query, with the most relevant on top.
# Pages should be identified by their URLs.

# Ranking: at the very least, your ranking formula should include tf-idf scoring, and take the important words into consideration, but you should feel free to add additional components to this formula if you think they improve the retrieval.

# IMPORT OTHER CLASSES HERE
import re
import json
class Search:

    def readIndexOfIndex(self):
        f = open("test_files/index_of_index.json")
        self.tokenIndexJson = json.load(f)
        f.close()
    def tokenize(self):
        pattern = "\s+"
        return re.split(pattern,self.query)

    def __init__(self, query):
        self.query = query
        self.indexfile = open("test_files/merged.txt","r")
        tokens = self.tokenize();
        print(tokens)
        # parse the index_of_index.json into a python dict
        # and save the result in tokenIndexJson
        self.readIndexOfIndex()
        self.results = dict()
        for token in tokens:
            if token in self.tokenIndexJson:
                pos = self.tokenIndexJson[token]
                self.indexfile.seek(pos)
                jsonline = self.indexfile.readline()
                print("jsonline",jsonline)
                jsonline = json.loads(jsonline)
                postings = jsonline[token]
                newdict = dict()

                # if the result dictionary is empty
                if not bool(self.results):
                    for docId in postings:
                        newdict[docId] = {token:postings[docId]}
                    self.results = newdict
                # if not empty
                else:
                    for docId in postings:
                        if docId in self.results:
                            newdict[docId] = self.results[docId]
                            newdict[docId][token] = postings[docId]
                    self.results = newdict
        print(self.results)





if __name__ == '__main__':
    search = Search("apple bbb")