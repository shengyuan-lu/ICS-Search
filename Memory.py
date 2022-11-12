import json
from os.path import getsize
import os
import shutil
from Reader import Reader, NoMoreFilesToReadException
from Parser import parse
from Tokenizer import compute_word_frequencies

class Memory:

    # initialize the master dict
    # initialize the document count
    def __init__(self):
        self.index = dict()
        self.doc_count = 0
        self.index_file_num = 0
        self.max_doc_ct = 50
        self.index_size = -1

    # this method will add the tokens from one page into the master dict
    # This will take in ({tokens:[occurrences, [position]]}, doc_id) and then update the internal index
    def add_page(self, token: 'dict[str:[int, [int]]]', doc_id: 'int'):

        # increment doc count
        self.doc_count += 1

        # insert / update master dict with token
        for key, val in token.items():
            # TODO for M1, we only care about freq for any given file
            if key not in self.index:
                self.index[key] = [[doc_id, val["freq"]]]
            else:
                self.index[key].append([doc_id, val["freq"]])

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

        path = "index"
        
        # Create the directory if not exist
        complete_name = os.path.join(path,f"indexfile{self.index_file_num}.json")

        with open(complete_name, 'w') as file:

            file.write('[')

            for index, item in enumerate(sorted(self.index.keys())):

                s = "{" + f'"{item}" : {self.index[item]}' + "}"

                if index != len(self.index.keys()) - 1:
                    s += ", \n"

                file.write(s)

            # json.dump(self.index, file, sort_keys = True, separators=["\n", ":"])

            file.write("]")

        self.index_size = getsize(complete_name)

        self.index_file_num += 1

    def print_stats(self):
        """
        Output the stats of the index to console\n
        # unique tokens, # unique docs, size of index on disk
        """
        # Get size of index on disk
        size = int(self.index_size)
        kb = int(size / 1000)

        # Format size to KB
        kb = f'{kb}.{int(size % 1000)}KB'

        stat_str = f'Unique token count: {len(self.index)}\n'
        stat_str += f'Unique document count: {self.doc_count}\n'
        stat_str += f'Index size on disk: {kb}'

        print(stat_str)

        with open('stats.txt', 'w+') as stats:
            stats.write(stat_str)


if __name__ == '__main__':
    reader = Reader('DEV_SMALL')
    memory = Memory()

    path = 'Index'

    # Remove the folder and its content if already exist
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create the folder
    os.mkdir(path)

    try:
        while True:
            file = reader.get_next_file()

            doc_id, url, raw_text = parse(file)

            frequencies = compute_word_frequencies(raw_text)

            memory.add_page(frequencies, doc_id)

    except NoMoreFilesToReadException as e:
        print(e)

    # Write index to disk
    memory.store_to_disk()

    # Print the stats
    memory.print_stats()