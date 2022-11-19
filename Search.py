# GOAL For Search

# Your program should prompt the user for a query.
# This doesn’t need to be a Web interface, it can be a console prompt.
# At the time of the query, your program will stem the query terms, look up your index, perform some calculations (see ranking below) and give out the ranked list of pages that are relevant for the query, with the most relevant on top.
# Pages should be identified by their URLs.

# Ranking: at the very least, your ranking formula should include tf-idf scoring, and take the important words into consideration, but you should feel free to add additional components to this formula if you think they improve the retrieval.

# IMPORT OTHER CLASSES HERE
import re
import json
import os
from nltk.stem import PorterStemmer
class Search:

    def readIndexOfIndex(self):
        f = open("index_of_index.json")
        self.tokenIndexJson = json.load(f)
        f.close()
    def tokenize(self):
        pattern = "\s+"
        return re.split(pattern,self.query)

    def readDocIdDict(self):
        f = open("doc_id_dict.json")
        self.idToUrl = json.load(f)
        f.close()

    def printResults(self,limit = 5):
        count = 0

        for r in self.sortedResults[0:limit]:
            print(r[1]["url"])





    def sortResults(self):
        self.sortedResults = sorted(self.results.items(), key=lambda t: -t[1]["score"])

    def __init__(self, query):
        self.query = query
        complete_name = os.path.join("Index", "final_index.txt")
        self.indexfile = open(complete_name,"r")
        tokens = self.tokenize();
        print(tokens)
        ps = PorterStemmer()
        # parse the index_of_index.json into a python dict
        # and save the result in tokenIndexJson
        self.readIndexOfIndex()
        self.results = dict()
        self.readDocIdDict()
        for token in tokens:
            stemmed_token = ps.stem(token)
            if stemmed_token in self.tokenIndexJson:
                pos = self.tokenIndexJson[stemmed_token]
                self.indexfile.seek(pos)
                jsonline = self.indexfile.readline()

                jsonline = json.loads(jsonline)
                postings = jsonline[stemmed_token]
                newdict = dict()

                # if the result dictionary is empty
                if not bool(self.results):
                    for docId in postings:

                        newdict[docId] = {token:postings[docId]}
                        newdict[docId]["url"] = self.idToUrl[docId]
                        newdict[docId]["score"] = postings[docId]
                    self.results = newdict
                # if not empty
                else:
                    for docId in postings:
                        #docId = self.idToUrl[docId]
                        if docId in self.results:

                            newdict[docId] = self.results[docId]
                            newdict[docId]["url"] = self.idToUrl[docId]
                            newdict[docId][token] = postings[docId]
                            newdict[docId]["score"] += postings[docId]
                    self.results = newdict
        self.sortResults()
        self.printResults()





if __name__ == '__main__':
    search = Search("informatics")