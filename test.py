import re

# 5/6/2023 log: Multiline string can now be split into paragraphs.
def check_update(old):
    arr = old.strip()
    test = re.split(r'\n', arr)
    test2 = []
    for paragraph in test:
        test2.append(re.split(r'\. ', paragraph.strip()))
    for paragraph in test2:
        for sentence in paragraph:
            sentence2 = re.sub(r'\.', '', sentence)
            print(f"{sentence2}")
    
  


check_update(
"""Tom likes Harry. 
Harry likes Jane. But Susan Loves Harry.
Jane dislikes Tom.""")