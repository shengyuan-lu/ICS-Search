import json
import os
from os import listdir, path, remove

def merger(path1 : str, path2 : str, out_path : str = "final_index.json",
           delete = False):
    """
    Merges two text files line by line, without loading either fully into RAM

    :param path1: The path to the first file to merge
    :param path2: The path to the second file to merge
    :param out_path: The path to the final, merged file
    :param delete: whether or not to delete the file
    :return: Void
    """

    #if we're merging with the output file, need to copy it into a temp first
    if path2 == out_path:
        new = open("temp.json", "w")
        with open(out_path, "r") as out:
            txt = ""
            for line in out:
                txt += line.strip() + "\n"
                new.write(line.strip() + "\n")
        #print("Wrote to new", txt)
        new.close()
        path2 = "temp.json"

    out = open(out_path, "w")
    print(f"Opening and merging {path1} with {path2}. Out path was {out_path}.\nPath 1 read: ")
    print_txt(path1)
    print("\nAnd Path 2 read:")
    print_txt(path2)
    with open(path1, "r") as a, open(path2, "r") as b:
        a_line = a.readline().strip()
        b_line = b.readline().strip()
        while True:
            #The line to write to the output
            line = ""
            if a_line == "" and b_line == "":
                break
            # print(a_line, "\tB line: ", b_line)
            aword, bword = "", ""
            a_json, b_json = None, None
            if a_line != "":
                a_json = json.loads(a_line)
                aword = list(a_json.keys())[0]
            if b_line != "":
                b_json = json.loads(b_line)
                bword = list(b_json.keys())[0]
            print(f"Comparing {aword} to {bword}")
            # if the words are the same, combine lists
            if aword == bword:
                a_json[aword] = a_json[aword] | b_json[bword]
                line = json.dumps(a_json)
                a_line = a.readline().strip()
                b_line = b.readline().strip()
                #print("A and B both equalled", aword)
            #If A is blank, but b isn't
            elif aword == "" and bword != "":
                line = json.dumps(b_json)
                b_line = b.readline().strip()
                print("A was blank, B wasn't")
            elif bword == "" and aword != "":
                line = json.dumps(a_json)
                a_line = a.readline().strip()
                print("B was blank, A wasn't", line)
            # if aword comes first alphabetically
            elif aword < bword:

                line = json.dumps(a_json)
                a_line = a.readline().strip()
                print(f"A came first, since {aword} comes before {bword}")
            #if bword comes first alphabetically
            elif bword < aword:
                line = json.dumps(b_json)
                b_line = b.readline().strip()
                #print(f"B came first, since {bword} comes before {aword}")
            #else:
                #print(f"ERROR in A: {aword}, B: {bword}")
            #print(aword, "\tB line: ", bword)
            out.write(line + "\n")
            #break
    out.close()
    print("Output read:")
    print_txt(out_path)
    #Check 'delete' bool before deleting
    if delete == False:
        return
    if path2 != "final_index.json":
        os.remove(path2)
    os.remove(path1)
    #delete path1 and path2 after done

def merge_folder(folder):
    """
    Merges all of the contents of a folder together
    :param folder: the folder to merge all of the contents of
    :return:
    """
    files = [i for i in listdir(folder) if ".json" in i]
    #don't merge if there is 0 or 1 files
    if len(files) < 2:
        return

    for f in files:
        f = path.join(folder, f)
        #print(f"Merging {f} with final_index")
        merger(f, "final_index.json", delete=True)
        #break

    print(files)

def print_txt(path):
    with open(path, "r") as f:
        print(f.read())


if __name__ == "__main__":
    f = open("final_index.json", "w")
    f.write("")
    f.close()

    merge_folder("test_files")
    #merger("test_files/index1.json", "test_files/index2.json", "final_index.json")