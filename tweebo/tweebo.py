'''
Python API to the TweeboParser. Module only caontains one function:
1. process_texts - Given a list of texts will process each text through \
TweeboParser and return a list of the same size in two different output \
formats: 1. CoNLL and 2. Stanford.
'''

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


def _to_conll(result_fp):
    '''
    :param result_fp: path to the file that contains `CoNLL formatted\
    <http://universaldependencies.org/format.html>`_ \
    dependency data. Where each tweet is seprated by a line.
    :type result_fp: Path
    :return: A list of Strings where each String is each Tweets CoNLL \
    output. If the Tweet was empty e.g. `` then `` will be returned.
    :rtype: list[str]
    '''
    conll_strings = []
    conll_string = []
    last_line = None
    with result_fp.open('r', encoding='utf-8') as result_file:

        for line in result_file:
            line = line.strip()
            if last_line == '' and line == '':
                continue
            elif line == '':
                # If empty sentence then add empty String
                if conll_string == [EMPTY_TOKEN]:
                    conll_strings.append('')
                else:
                    conll_strings.append('\n'.join(conll_string))
                conll_string = []
            else:
                line_data = line.split('\t')
                token_text = line_data[1].strip()
                if token_text == EMPTY_TOKEN:
                    conll_string.append(EMPTY_TOKEN)
                else:
                    conll_string.append(line)
            last_line = line
        return conll_strings


def _to_stanford(result_fp):
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


def process_texts(texts, output_type='conll'):
    '''
    :param texts: List of Strings that to dependency parse with Tweebo
    :param output_type: String specifying the output type. Either `stanford` \
    or `conll`.
    :type texts: list[str]
    :type output_type: str
    :return: Depending on the output_type for `stanford` see \
    :py:func:`_to_stanford`. For conll see :py:func:`_to_conll`
    :rtype: either list[Dict] or list[str]
    :raises TypeError: If the texts are not a list of Strings or unicode \
    Strings.
    :raises ValueError: If the output_type is not equal to `stanford` or \
    `conll`
    '''

    if not isinstance(texts, list):
        raise TypeError('Expected texts to be of type list not {}'
                        .format(type(texts)))

    allowed_output_types = ['stanford', 'conll']
    output_type = output_type.lower()
    if output_type not in allowed_output_types:
        raise ValueError('output_type has to be one of the following: {}\n'
                         'Not {}'.format(allowed_output_types, output_type))
    temp_dir_fp = tempfile.mkdtemp()
    try:
        text_fp = Path(temp_dir_fp, 'text_file.txt')
        # Add the data to the text file
        with text_fp.open('w', encoding='utf-8') as text_file:
            for index, text in enumerate(texts):
                if isinstance(text, str):
                    text = text.decode('utf-8')
                elif not isinstance(text, unicode):
                    raise TypeError('The Strings in text must be of '
                                    'str or unicode not {}'
                                    .format(type(text)))
                print(text)
                text = text.strip()
                if not text:
                    print('does this happen')
                    text_file.write(EMPTY_TOKEN)
                else:
                    text_file.write(text)
                if index != (len(texts) - 1):
                    text_file.write(u'\n')
        _process_file(text_fp)
        result_fp = Path(temp_dir_fp, 'text_file.txt.predict')
        if output_type == 'stanford':
            return _to_stanford(result_fp)
        else:
            return _to_conll(result_fp)
    except Exception as error:
        shutil.rmtree(temp_dir_fp)
        raise error
    else:
        shutil.rmtree(temp_dir_fp)
