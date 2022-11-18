# GOAL For Indexer
import json

# Create an inverted index for the given corpus with data structures designed by you.

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.


# IMPORT OTHER CLASSES HERE
from Reader import Reader, NoMoreFilesToReadException
from Memory import Memory
from Parser import parse
from Tokenizer import compute_word_frequencies
import os
import shutil
import json


class Indexer:

    def __init__(self, base_folder):
        self.base_folder = base_folder


    def generate_index_of_index(self, merged_index_path):

        # The file name of the generated json file
        index_of_index_file_name = 'index_of_index.json'

        # Check if the merged index path is valid
        if os.path.isfile(merged_index_path):

            # Make a new word : char_count dict
            lookup = dict()

            # Init char count
            char_count = 0

            # Open the merged index in read only mode
            with open(merged_index_path, 'r') as index:

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

            print(f'{index_of_index_file_name} is successfully generated')

        else:
            print(f'Warning: {merged_index_path} does not exist. No {index_of_index_file_name} is generated')


    def run(self):
        reader = Reader(self.base_folder)
        memory = Memory()

        path = 'Index'

        # Remove the folder and its content if already exist
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            # Create the folder
            os.mkdir(path)

        if os.path.exists('reader_stats.txt'):
            os.remove('reader_stats.txt')

        if os.path.exists('memory_stats.txt'):
            os.remove('memory_stats.txt')

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

        except NoMoreFilesToReadException as e:
            print(e)

            with open('reader_stats.txt', 'w+') as stats:
                stats.write(str(e))

        # Write index to disk
        memory.store_to_disk()

        # Print the stats
        memory.print_stats()


# The actual main function to generate the index
if __name__ == '__main__':
    indexer = Indexer('DEV')
    indexer.run()
    indexer.generate_index_of_index('Index/indexfile0.txt')
    # indexer.generate_index_of_index('test_files/merged.txt')
