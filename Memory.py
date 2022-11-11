import json
from os.path import getsize


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
        # this check if the index have anything in it, and then only save to disk if there is something in it
        if len(self.index) <= 0:
            return

        with open(f"indexfile{self.index_file_num}.json", 'w') as file:

            file.write('[')

            for index, item in enumerate(sorted(self.index.keys())):

                s = "{" + f'"{item}" : {self.index[item]}' + "}"

                if index != len(self.index.keys()) - 1:
                    s += ", \n"

                file.write(s)

            # json.dump(self.index, file, sort_keys = True, separators=["\n", ":"])

            file.write("]")

        self.index_size = getsize(f"indexfile{self.index_file_num}.json")
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
        kb = f"{kb}.{int(size % 1000)}KB"
        print(f"Wrote index to disk. Had {len(self.index)} unique tokens.\n"
              f"Had {self.doc_count} unique documents. Index took up {kb} on disk")


# Only for testing purposes
if __name__ == '__main__':
    dit = {"capple": [5, [2, 3]], "bapple": [4, [5, 3]]}

    mem = Memory()
    mem.store_to_disk()
    mem.add_page(dit, 1)
    mem.store_to_disk()
