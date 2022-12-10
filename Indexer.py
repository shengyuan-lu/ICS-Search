from Reader import Reader, NoMoreFilesToReadException
from Memory import Memory
from Parser import parse
from Merger import merge_folder
from Tokenizer import compute_word_frequencies
from os import path
import os
import shutil
import json
import time


class Indexer:

    def __init__(self, source_folder, base_folder, merged_index_name):
        self.source_folder = source_folder
        self.base_folder = base_folder
        self.merged_index_path =  path.join(base_folder, merged_index_name)


    def generate_index_of_index(self):

        # The file name of the generated json file
        index_of_index_file_name = 'index_of_index.json'

        # Check if the merged index path is valid
        if os.path.isfile(self.merged_index_path):

            # Make a new word : char_count dict
            lookup = dict()

            # Init char count
            char_count = 0

            # Open the merged index in read only mode
            with open(self.merged_index_path, 'r') as index:

                # Read every line until there's no more line to read
                try:
                    while True:
                        line = index.readline()

                        word_obj = json.loads(str(line))

                        word = list(word_obj.keys())[0]

                        lookup[word] = char_count

                        char_count += len(line)

                except:
                    # Catch the exception thrown from the .readline()
                    pass

            # Remove the index of index from last run, if the file exist
            if os.path.isfile(index_of_index_file_name):
                os.remove(index_of_index_file_name)

            # Open the index_of_index.json in write mode, create one if not exist
            with open(index_of_index_file_name, 'w+') as index_of_index:
                # Write the word : char_count to the json
                index_of_index.write(json.dumps(lookup, sort_keys=True, indent=4))

            print()
            log = f'Indexer: {index_of_index_file_name} is successfully generated'
            print(log)

            with open('indexer_stats.txt', 'w+') as stats:
                stats.write(log + '\n')

        else:
            print(f'Indexer Warning: {self.merged_index_path} does not exist. No {index_of_index_file_name} is generated')


    def run(self):

        index_start_time = time.time()

        reader = Reader(self.source_folder)
        memory = Memory()

        # Path of the raw Index being generated
        path = self.base_folder

        # Remove the folder and its content if already exist
        if os.path.exists(path):
            shutil.rmtree(path)

        os.mkdir(path)

        if os.path.exists('reader_stats.txt'):
            os.remove('reader_stats.txt')

        if os.path.exists('memory_stats.txt'):
            os.remove('memory_stats.txt')

        if os.path.exists('indexer_stats.txt'):
            os.remove('indexer_stats.txt')

        try:
            while True:
                # Get next json file from the reader class
                file = reader.get_next_file()

                # Parse the json file to get doc_id, url, and raw content
                doc_id, url, raw_text = parse(file)

                # Calculate the word frequency
                frequencies = compute_word_frequencies(raw_text)

                # Store the result to the memory
                memory.add_page(frequencies, doc_id)

        except NoMoreFilesToReadException as error:
            print(error)

            with open('reader_stats.txt', 'w+') as stats:
                stats.write(str(error))

        # Write index to disk
        memory.store_to_disk()

        # Print the stats
        memory.print_stats()

        # Merge everything under /Index
        merge_folder(path)

        self.generate_index_of_index()

        index_finish_time = time.time()

        with open('indexer_stats.txt', 'a+') as stats:
            time_lapse_log = 'Indexer: ' + str('%.2f' % ((index_finish_time - index_start_time)/60)) + ' minutes used to build index'
            print(time_lapse_log)
            stats.write(time_lapse_log)


# The actual main function to generate the index
if __name__ == '__main__':
    indexer = Indexer('DEV', 'Index', 'final_index.txt')
    indexer.run()
