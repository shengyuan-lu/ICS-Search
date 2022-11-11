import json


class Memory:

    #initialize the master dict
    #initialize the document count
    def __init__(self):
        self.index = dict()
        self.doc_count = 0
        self.index_file_num = 0
        self.max_doc_ct = 50


    # this method will add the tokens from one page into the master dict
    # This will take in ({tokens:[occurences, [position]]}, doc_id) and then update the internal index
    def add_page(self, tok:dict[str:[int, [int]]], doc_id:int):

        # increment doc count
        self.doc_count += 1

        # insert / update master dict with token
        for key,val in tok.items():
            if key not in self.index:
                self.index[key] = [[doc_id, val[0], val[1]]]
            else:
                self.index[key].append([doc_id, val[0], val[1]])
        
        # check if doc_count is at max_doc_ct and store to disk if so
        if self.doc_count == self.max_doc_ct:
            self.doc_count = 0
            self.store_to_disk()
            

    # this method will store the index to a file on disk (not fully implemented yet to search through)
    def store_to_disk(self):

        # this check if the index have anything in it, and then only save to disk if there is something in it
        if len(self.index) > 0:
            with open(f"indexfile{self.index_file_num}.json", 'w') as file:
                json.dump(self.index, file, sort_keys = True)
            self.index_file_num += 1
        

if __name__ == '__main__':

    dit = {"capple":[5, [2,3]], "bapple":[4, [5,3]]}

    mem = Memory()
    mem.store_to_disk()
    mem.add_page(dit, 1)
    mem.store_to_disk()
