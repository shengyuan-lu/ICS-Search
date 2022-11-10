import json


class Memory:
    def __init__(self):
        self.index = dict()
        self.doc_count = 0

    def add_page(self, tok:dict[str:[int, int]], url:str):
        self.doc_count += 1
        for key,val in tok:
            if key in self.index:
                self.index[key] = [[url, val[0], val[1]]]
            else:
                self.index[key].append([url, val[0], val[1]])
        
        if self.doc_count == 50:
            self.doc_count = 0

if __name__ == 'main':
    dit = {"AB":[1,2,3], "B":[2,3,4], "CD":[3,4,5]}
    dit["AA"] = [1,1,1]
    dit["BB"] = [2,3,5]
    dit = sorted(dit)
    f = open("test.txt", 'w')
    json.dump(dit, f)