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
if not text_only_file.is_file():
    with data_path.open('r') as read_data:
        with text_only_file.open('w') as write_file:
            for line in read_data:
                if line.strip():
                    write_file.write(line)

test_data_dir = Path(__file__).absolute().parent.resolve()
data_file = test_data_dir.joinpath('..', '..', 'ark-tweet-nlp-0.3.2', 'data',
                                   'twpos-data-v0.3', 'oct27.splits',
                                   'oct27.train')
tweets_file = test_data_dir.joinpath('tweets.txt')
if not tweets_file.is_file():
    count = 0
    with tweets_file.open('w', encoding='utf-8') as tweet_data:
        with data_file.open('r', encoding='utf-8') as lines:
            for line in lines:
                line = line.strip()
                if line:
                    word = line.split()[0]
                    tweet_data.write(u'{} '.format(word))
                else:
                    tweet_data.write(u'\n')
                    count += 1
                    if count == 3:
                        break
