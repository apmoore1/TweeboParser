'''
Given the Sherlock Holmes book The Adventures of Sherlock Holmes, \
by Arthur Conan Doyle form Project Gutenberg's. It saves all of the lines \
in the book that contains text to the "sherlock_holmes_text_only.txt" file. \


This file will be used to test the parser from each commit to see if a given \
commit has changed the functionality of the parser.
'''

from pathlib import Path

data_path = Path('sherlock_holmes.txt')
text_only_file = Path('sherlock_holmes_text_only.txt')
with data_path.open('r') as read_data:
    with text_only_file.open('w') as write_file:
        for line in read_data:
            if line.strip():
                write_file.write(line)
