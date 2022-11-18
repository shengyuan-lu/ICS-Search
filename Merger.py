import json
import os
from os import listdir, path, remove


def merger(path1: str, path2: str, out_path: str = "final_index.json",
           delete: bool = False):
    """
    Merges two text files line by line, without loading either fully into RAM

    :param path1: The path to the first file to merge
    :param path2: The path to the second file to merge
    :param out_path: The path to the final, merged file
    :param delete: whether or not to delete the files after
    :return: Void
    """

    # if we're merging with the output file, need to copy it into a temp first
    if path2 == out_path:
        new = open("temp.json", "w")
        with open(out_path, "r") as out:
            #Copy each line to the output
            for line in out:
                new.write(line.strip() + "\n")
        new.close()
        #Merge with the old merged file
        path2 = "temp.json"

    out = open(out_path, "w")

    #Open each file line by line, don't load either fully into RAM
    with open(path1, "r") as a, open(path2, "r") as b:
        #Get the first lines of both files
        a_line = a.readline().strip()
        b_line = b.readline().strip()
        #Iterate until both files are fully read
        while True:
            # The line to write to the output
            line = ""
            #End when both lines are blank
            if a_line == "" and b_line == "":
                break

            aword, bword = "", ""
            a_json, b_json = None, None
            #Load the jsons if not blank, get the word on that line
            if a_line != "":
                a_json = json.loads(a_line)
                aword = list(a_json.keys())[0]
            if b_line != "":
                b_json = json.loads(b_line)
                bword = list(b_json.keys())[0]

            # if the words are the same, combine lists
            if aword == bword:
                #Merge dicts
                a_json[aword] = a_json[aword] | b_json[bword]
                line = json.dumps(a_json)
                a_line = a.readline().strip()
                b_line = b.readline().strip()

            # If A is blank, but b isn't
            elif aword == "" and bword != "":
                line = json.dumps(b_json)
                b_line = b.readline().strip()

            elif bword == "" and aword != "":
                line = json.dumps(a_json)
                a_line = a.readline().strip()

            # if aword comes first alphabetically
            elif aword < bword:

                line = json.dumps(a_json)
                a_line = a.readline().strip()

            # if bword comes first alphabetically
            elif bword < aword:
                line = json.dumps(b_json)
                b_line = b.readline().strip()

            #Write the new, merged line to the output
            out.write(line.strip() + "\n")
    #Close the output
    out.close()

    # Check 'delete' bool before deleting
    if delete == False:
        return
    # delete path1 and path2 after done
    if path2 != "final_index.json":
        os.remove(path2)
    os.remove(path1)



def merge_folder(folder):
    """
    Merges all of the contents of a folder together
    :param folder: the folder to merge all of the contents of
    :return:
    """
    # Only parse files that end in .txt. Also eliminates dirs
    files = [i for i in listdir(folder) if ".txt" in i]

    # Merge every file into the final_index on by one
    for f in files:
        # Create the full path
        f = path.join(folder, f)
        # Equivalent of += by calling final_index for input 2 and output
        merger(f, "final_index.json", "final_index.json", delete=False)
    # Delete the temp.json if it still exists
    if os.path.exists("temp.json"):
        os.remove("temp.json")
    print(f"Merged the {len(files)} file(s) in {folder}")

def print_txt(path):
    with open(path, "r") as f:
        print(f.read())


if __name__ == "__main__":
    f = open("final_index.json", "w")
    f.write("")
    f.close()

    merge_folder("test_files")
    # merger("test_files/index1.json", "test_files/index2.json", "final_index.json")
