import json
from os.path import getsize
import os

class Memory:

    # initialize the master dict
    # initialize the document count
    def __init__(self):

        # This is index in Memory
        self.index = dict()
        # This is amount of docs in the index in Memory
        self.doc_count = 0
        # This is amount of index files on disk
        self.index_file_num = 0
        # This is max amount of docs that can be stored in the index in Memory before getting written to disk and wiped from memory
        self.max_doc_ct = 500
        # This is the total number of docs that are added to indexes
        self.total_doc_count = 0
        # This is the total size of the generated indexes
        self.index_size = 0
        # This is the set of unique tokens that are in the index
        self.uniq_tokens = set()


    # this method will add the tokens from one page into the master dict
    # This will take in ({tokens:[occurrences, [position]]}, doc_id) and then update the internal index
    def add_page(self, token: 'dict[str:[int, [int]]]', doc_id: 'int'):

        # increment doc count and total_doc_count
        self.doc_count += 1
        self.total_doc_count += 1

        # insert / update master dict with token
        for key, val in token.items():
            # TODO for M1/M2, we only care about freq for any given file
            if key not in self.index:
                self.index[key] = {doc_id: val["freq"]}
            else:
                self.index[key][doc_id] = val["freq"]

            if key not in self.uniq_tokens:
                self.uniq_tokens.add(key)

        # check if doc_count is at max_doc_ct and store to disk if so
        if self.doc_count == self.max_doc_ct:
            self.doc_count = 0
            self.store_to_disk()


    # this method will store the index to a file on disk (not fully implemented yet to search through)
    def store_to_disk(self):
        """
        Writes the current in-memory index to disk
        """
        # This check if the index have anything in it, and then only save to disk if there is something in it
        if len(self.index) <= 0:
            return
        
        # Create the directory if not exist
        complete_name = os.path.join("Index", f"indexfile{self.index_file_num}.txt")

        with open(complete_name, 'w') as file:

            for index, item in enumerate(sorted(self.index.keys())):

                s = {item:self.index[item]}

                file.write(json.dumps(s))

                file.write("\n")

            # file.write(json.dumps(self.index, sort_keys=True))

            # file.write(json.dumps(self.index, sort_keys=True, indent=4))

        self.index_size += getsize(complete_name)

        self.index_file_num += 1

        self.index.clear()


    def print_stats(self):
        """
        Output the stats of the index to console\n
        # unique tokens, # unique docs, size of index on disk
        """
        # Get size of index on disk
        size = int(self.index_size)
        kb = int(size / 1000)

        # Format size to KB
        kb = f'{kb}.{int(size % 1000)} KB'

        stat_str = f'Memory: Unique token count: {len(self.uniq_tokens)}\n'
        stat_str += f'Memory: Unique document count: {self.total_doc_count}\n'
        stat_str += f'Memory: Total separated index size on disk: {kb}'

        print()
        print(stat_str)

        with open('memory_stats.txt', 'w+') as stats:
            stats.write(stat_str)