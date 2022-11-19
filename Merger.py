import json
import os
from os.path import getsize
from os import listdir, path, remove


def merger(path1: str, path2: str, out_path: str = 'Index/final_index.txt',
           delete: bool = False):
    """
    Merges two text files line by line, without loading either fully into RAM

    :param path1: The path to the first file to merge
    :param path2: The path to the second file to merge
    :param out_path: The path to the final, merged file
    :param delete: whether or not to delete the files after
    :return: Void
    """
    # Create out_put_path if not exist
    if not os.path.exists(out_path):
        open(out_path,'w+')

    # If we're merging with the output file, need to copy it into a temp first
    if path2 == out_path:
        new = open('temp.json', 'w')

        with open(out_path, 'r') as out:
            #Copy each line to the output
            for line in out:
                new.write(line.strip() + '\n')

        new.close()

        # Merge with the old merged file
        path2 = 'temp.json'

    out = open(out_path, 'w')

    #Open each file line by line, don't load either fully into RAM
    with open(path1, 'r') as a, open(path2, 'r') as b:
        #Get the first lines of both files
        a_line = a.readline().strip()
        b_line = b.readline().strip()
        #Iterate until both files are fully read
        while True:
            # The line to write to the output
            line = ''
            #End when both lines are blank
            if a_line == '' and b_line == '':
                break

            a_word, b_word = '', ''
            a_json, b_json = None, None

            #Load the jsons if not blank, get the word on that line
            if a_line != '':
                a_json = json.loads(a_line)
                a_word = list(a_json.keys())[0]

            if b_line != '':
                b_json = json.loads(b_line)
                b_word = list(b_json.keys())[0]

            # if the words are the same, combine lists
            if a_word == b_word:
                #Merge dicts
                a_json[a_word] = a_json[a_word] | b_json[b_word]
                line = json.dumps(a_json)
                a_line = a.readline().strip()
                b_line = b.readline().strip()

            # If A is blank, but b isn't
            elif a_word == '' and b_word != '':
                line = json.dumps(b_json)
                b_line = b.readline().strip()

            elif b_word == '' and a_word != '':
                line = json.dumps(a_json)
                a_line = a.readline().strip()

            # if a_word comes first alphabetically
            elif a_word < b_word:

                line = json.dumps(a_json)
                a_line = a.readline().strip()

            # if b_word comes first alphabetically
            elif b_word < a_word:
                line = json.dumps(b_json)
                b_line = b.readline().strip()

            #Write the new, merged line to the output
            out.write(line.strip() + '\n')

    #Close the output
    out.close()

    # Check 'delete' bool before deleting
    if not delete:
        return

    # Delete path1 and path2 after done
    if path2 != 'final_index.txt':
        os.remove(path2)

    os.remove(path1)



def merge_folder(folder):
    """
    Merges all of the contents of a folder together
    :param folder: the folder to merge all of the contents of
    :return:
    """
    print()
    print(f'Merger: Started merging indexes under /{folder}')

    final_index_path = path.join(folder, 'final_index.txt')
    
    # Only parse files that end in .txt. Also eliminates dirs
    files_list = [i for i in listdir(folder) if i.endswith('.txt')]

    # Merge every file into the final_index on by one
    for file in files_list:
        # Create the full path
        file = path.join(folder, file)

        # Equivalent of += by calling final_index for input 2 and output
        merger(file, final_index_path, final_index_path, delete=True)

    # Delete the temp.json if it still exists
    if os.path.exists('temp.json'):
        os.remove('temp.json')

    # Get size of index on disk
    size = int(getsize(final_index_path))
    kb = int(size / 1000)

    # Format size to KB
    kb = f'{kb}.{int(size % 1000)} KB'

    print(f'Merger: Finished merging {len(files_list)} files in /{folder}')
    print(f'Merger: Merged index size on disk: {kb}')



# def print_txt(path):
    # with open(path, 'r') as file:
         # print(file.read())


if __name__ == '__main__':
    f = open('final_index.txt', 'w')
    f.write('')
    f.close()

    merge_folder('test_files')
    # merger('test_files/index1.json', 'test_files/index2.json', 'final_index.txt')
