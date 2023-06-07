import re

# 5/6/2023 log: Multiline string can now be split into paragraphs.
# 6/6/2023 log: Properly turned body into nested arrays and added/removed 
# checking
# 7/6/2023 log: Parsed results into list of dicts. Issue found is 
# check_changes() returning false negatives if the sentences are the 
# same but their positions are swapped around
def track_changes(old, new):
    old_array = body_to_array(old)
    new_array = body_to_array(new)
    check_changes(old_array, new_array)
    return print("done")

def body_to_array(body):
    # Turn body into array of paragraphs
    paragraphs = re.split(r'\n', body)
    sentences = []
    # Turn paragraphs into sentences. Each sentence is in an array
    # nested in another array.
    for paragraph in paragraphs:
        sentences.append(re.split(r'(?<=[\.\!\?])\s+', paragraph.strip()))
    print(sentences)
    return sentences

def check_changes(old, new):
    added = []
    removed = []
    # First, check if any paragraphs were removed
    for i in range(len(old)):
        for j in range(len(old[i])):
            found = False
            repeated = False
            for k in range(len(new)):
                for l in range(len(new[k])):
                    # As long as the sentence is somewhere, we can 
                    # take it as unedited. If there are no matches,
                    # it is removed/edited
                    if (old[i][j] == new[k][l]) and (i == k):
                        found = True
            if not found and not repeated:
                repeated = True
                line_number = 0
                for j in range(i):
                    line_number += len(old[j])
                line_number += j + 1
                removed.append({"line_number": line_number, "sentence": old[i][j]})
    # Next, check if any paragraphs were added
    for i in range(len(new)):
        for j in range(len(new[i])):
            found = False
            repeated = False
            for k in range(len(old)):
                for l in range(len(old[k])):
                    # As long as the sentence is somewhere, we can 
                    # take it as unedited. If there are no matches,
                    # it is added/edited
                    if (new[i][j] == old[k][l]) and (i == k):
                        found = True
            if not found and not repeated:
                repeated = True
                line_number = 0
                for j in range(i):
                    line_number += len(new[j])
                line_number += j + 1
                added.append({"line_number": line_number, "sentence": new[i][j]})            
    print(f"Added: {added}\nRemoved: {removed}")

track_changes("""Django is a web framework. It uses python as its backend and HTML as its frontend. It is well loved.
Django was built in 1983.""", """Django is a web framework. Django was built in 1983. 
It uses python as its backend and HTML as its frontend. It is well loved.""")