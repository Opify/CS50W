import re


def track_changes(old, new):
    """Takes in old and new body of text and checks if there is any changes in the contents of the body. 
    Returns array with sentences added followed by sentences removed. 
    Does NOT track if sentences have been moved."""
    old_array = body_to_array(old)
    new_array = body_to_array(new)
    return check_changes(old_array, new_array)

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
    return [added, removed]
