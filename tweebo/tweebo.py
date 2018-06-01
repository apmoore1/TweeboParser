from pathlib import Path
import tempfile
from traceback import format_exc
import shutil
import subprocess

EMPTY_TOKEN = u'$$$EMPTY$$$'


def _process_file(process_fp):
    '''
    :param process_fp: File to run through the dependency parser.
    :type process_fp: Path
    :return: None
    :raises SystemError: If the dependency parser run.sh script fails.
    '''

    this_dir = Path(__file__).absolute().parent.resolve()
    run_file = this_dir.joinpath('..', 'run.sh').resolve()
    try:
        sub_process_params = ['bash', str(run_file),
                              str(process_fp)]
        if subprocess.call(sub_process_params):
            raise SystemError('Could not run the Tweebo run script')

    except Exception as e:
        raise SystemError('Error {} during running the Tweebo run script, '
                          'Stack Trace:\n {}'.format(repr(e), format_exc()))


def _process_result(result_fp):
    '''
    :param result_fp: path to the file that contains `CoNLL formatted\
    <http://universaldependencies.org/format.html>`_ \
    dependency data. Where each tweet is seprated by a line.
    :type result_fp: Path
    :return: A list of dictionaries where each dictionary represents data \
    associated to one Tweet/text. Each dictionary contains 3 keys:
    1. index - The index of Tweet being processed e.g. first Tweet has index \
    value 0
    2. basicDependencies - Contains a list of dicts where each dict is \
    associated to a token and contains the following keys:
    2.1. dep - relation between the HEAD and the dependent word
    2.2. governor - index of the HEAD word where the index can be looked up \
    in the tokens
    2.3. governorGloss - HEAD word
    2.4. dependent - index of the dependent word
    2.5. dependentGloss - dependent word
    3. tokens - Contains a list of dicts where each dict contains detailed \
    information about each word/token in the tweet. The keys in the dicts:
    3.1. index - index of the word
    3.2. word - token word e.g. `Apple`
    3.3. originalText - same as word
    3.4. pos - POS tag of the word. Tagged by `Twokenizer \
    <http://www.cs.cmu.edu/~ark/TweetNLP/gimpel+etal.acl11.pdf>`_. POS tag \
    set is a Twitter specific one of which the tagset is explained in \
    the following `paper \
    <http://www.cs.cmu.edu/~ark/TweetNLP/gimpel+etal.acl11.pdf>`_.\
    The list will contain empty dicts if the string was empty e.g. ` `.\
    This dictionary structure is based off the output that you will recive \
    from the Stanford Dependency Parse through the Python API when using the \
    json response. Stanford Python link \
    `here <https://github.com/Lynten/stanford-corenlp>`_
    :rtype: list[Dict]
    '''

    def index_2_word(index, word_dicts):
        '''
        :param index: index of a word
        :param word_dicts: list of dicts where each dict represents \
        information about a word and contains at least two keys: `word` and \
        `index`
        :type index: int
        :type word_dicts: list[Dict]
        :return: Returns the word that has the index given associated to it \
        for the word_dicts.
        :rtype: str
        :raises ValueError: If the index is not in the word_dicts
        '''
        # 0 is always the special word ROOT
        # -1 means that the word is not included in the dependency tree
        # word returned for -1 == $$NAN$$
        if index == 0:
            return 'ROOT'
        elif index == -1:
            return '$$NAN$$'
        for word_dict in word_dicts:
            if index == word_dict['index']:
                return word_dict['word']
        raise ValueError('Cannot find word index: {} in the following word '
                         'information dictionaries: {}'
                         .format(index, word_dicts))

    tweets = []
    index = 0
    with result_fp.open('r', encoding='utf-8') as result_file:
        last_line = None
        tweet_data = {}
        basic_dependencies = []
        tokens = []
        for line in result_file:
            line = line.strip()
            if last_line == '' and line == '':
                continue
            elif line == '':
                # If empty sentence then add an empty list
                if basic_dependencies == [EMPTY_TOKEN]:
                    tweet_data['basicDependencies'] = []
                    tweet_data['tokens'] = []
                else:
                    # Need to add token data into the dependency inforamtion
                    temp_basic_dependencies = []
                    for dependecy_info in basic_dependencies:
                        gov_word = index_2_word(dependecy_info['governor'],
                                                tokens)
                        dep_word = index_2_word(dependecy_info['dependent'],
                                                tokens)
                        dependecy_info['governorGloss'] = gov_word
                        dependecy_info['dependentGloss'] = dep_word
                        temp_basic_dependencies.append(dependecy_info)
                    basic_dependencies = temp_basic_dependencies
                    tweet_data['basicDependencies'] = basic_dependencies
                    tweet_data['tokens'] = tokens
                tweet_data['index'] = index
                tweets.append(tweet_data)
                index += 1
                basic_dependencies = []
                tokens = []
                tweet_data = {}
            else:
                line = line.split('\t')
                token_text = line[1].strip()
                if token_text == EMPTY_TOKEN:
                    basic_dependencies.append(EMPTY_TOKEN)
                    tokens.append(EMPTY_TOKEN)
                else:
                    token_info = {}
                    token_info['index'] = int(line[0])
                    token_info['word'] = token_text
                    token_info['originalText'] = token_text
                    token_info['pos'] = line[4]
                    tokens.append(token_info)

                    dependecy_info = {}
                    relation = line[7]
                    dependecy_info['governor'] = int(line[6])
                    dependecy_info['dependent'] = int(line[0])
                    if dependecy_info['governor'] == 0:
                        relation = 'ROOT'
                    dependecy_info['dep'] = relation
                    if token_text == EMPTY_TOKEN:
                        basic_dependencies.append(EMPTY_TOKEN)
                    else:
                        basic_dependencies.append(dependecy_info)
            last_line = line
        return tweets


def process_texts(texts):
    '''
    :param texts: List of Strings that to dependency parse with Tweebo
    :type texts: list[str]
    :return: Dependency parsed Strings. See :py:func:`_process_result` return \
    for more details on the return value.
    :rtype: list[Dict]
    :raises TypeError: If the list of texts are not Strings or unicode strings
    '''

    temp_dir_fp = tempfile.mkdtemp()
    try:
        text_fp = Path(temp_dir_fp, 'text_file.txt')
        # Add the data to the text file
        with text_fp.open('w', encoding='utf-8') as text_file:
            for index, text in enumerate(texts):
                text = text.strip()
                if not text:
                    print('does this happen')
                    text_file.write(EMPTY_TOKEN)
                else:
                    if isinstance(text, str):
                        text = text.decode('utf-8')
                    elif not isinstance(text, unicode):
                        raise TypeError('The Strings in text must be of '
                                        'str or unicode not {}'
                                        .format(type(text)))
                    text_file.write(text)
                if index != (len(texts) - 1):
                    text_file.write(u'\n')
        _process_file(text_fp)
        result_fp = Path(temp_dir_fp, 'text_file.txt.predict')
        return _process_result(result_fp)

    except Exception as e:
        shutil.rmtree(temp_dir_fp)
        print('Error {} during running the Tweebo run script, '
              'Stack Trace:\n {}'.format(repr(e), format_exc()))
    else:
        shutil.rmtree(temp_dir_fp)
