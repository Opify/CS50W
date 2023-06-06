import re

# 5/6/2023 log: Multiline string can now be split into paragraphs.
# 6/6/2023 log: Properly turned body into nested arrays and added/removed 
# checking
def track_changes(old, new):
    old_array = body_to_array(old)
    new_array = body_to_array(new)
    check_changes(old_array, new_array)
    return print("done")

def body_to_array(body):
    # Turn body into array of paragraphs
    paragraphs = re.split(r'\n', body.strip())
    sentences = []
    # Turn paragraphs into sentences. Each sentence is in an array
    # nested in another array. strip() was needed due to empty strings
    # that are left in the array
    for paragraph in paragraphs:
        sentences.append(re.split(r'\.+ |\!+ |\?+ ', paragraph.strip()))
    print(sentences)
    return sentences

def check_changes(old, new):
    added = []
    removed = []
    edited = []
    # First, check if any paragraphs were removed
    for i in range(len(old)):
        for j in range(len(old[i])):
            found = False
            for k in range(len(new)):
                for l in range(len(new[k])):
                    # As long as the sentence is somewhere, we can 
                    # take it as unedited. If there are no matches,
                    # it is removed/edited
                    if old[i][j] == new[k][l]:
                        found = True
        if not found:
            removed.append(old[i][j])
    # Next, check if any paragraphs were added
    for i in range(len(new)):
        for j in range(len(new[i])):
            found = False
            for k in range(len(old)):
                for l in range(len(old[k])):
                    # As long as the sentence is somewhere, we can 
                    # take it as unedited. If there are no matches,
                    # it is added/edited
                    if new[i][j] == old[k][l]:
                        found = True
            if not found:
                added.append(new[i][j])
    print(f"Added: {added}, Removed: {removed}, Edited: {edited}")



track_changes("""Tom likes Jane. Mary likes Steven.""", """Tom likes Jane. Mary likes Steve.""")