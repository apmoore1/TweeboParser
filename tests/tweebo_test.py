# encoding: utf-8
'''
Tests all the functions within tweebo.tweebo through the method \
process_texts. The test functions within this module are the following:
1. test_process_texts_stanford - tests that the ouput of process_texts \
conforms to the Stanford styled output.
2. test_process_texts_stanford - tests that the ouput of process_texts \
conforms to the `CoNLL format\
<http://universaldependencies.org/format.html>`_
3. test_process_texts_exceptions - tests that the expected exceptions that \
should be raised do raise in the correct situtation
'''

import pytest

from tweebo import tweebo


def test_process_texts_stanford():
    '''
    Tests :py:func:`tweebo.process_texts` where the output type is stanford. \
    We perform the following tests:
    1. 2 unicode sentences
    2. 2 ASCII sentences
    3. 3 ASCII sentences where the 2nd sentence is empty.
    '''

    tokens_0 = [{'index': 1, 'word': u'I', 'originalText': u'I', 'pos': u'O'},
                {'index': 2, 'word': u'predict', 'originalText': u'predict',
                 'pos': u'V'},
                {'index': 3, 'word': u'I', 'originalText': u'I', 'pos': u'O'},
                {'index': 4, 'word': u"won't", 'originalText': u"won't",
                 'pos': u'V'},
                {'index': 5, 'word': u'win', 'originalText': u'win',
                 'pos': u'V'},
                {'index': 6, 'word': u'a', 'originalText': u'a', 'pos': u'D'},
                {'index': 7, 'word': u'single', 'originalText': u'single',
                 'pos': u'A'},
                {'index': 8, 'word': u'game', 'originalText': u'game',
                 'pos': u'N'},
                {'index': 9, 'word': u'I', 'originalText': u'I', 'pos': u'O'},
                {'index': 10, 'word': u'bet', 'originalText': u'bet',
                 'pos': u'V'},
                {'index': 11, 'word': u'on', 'originalText': u'on',
                 'pos': u'P'},
                {'index': 12, 'word': u'.', 'originalText': u'.', 'pos': u','},
                {'index': 13, 'word': u'Got', 'originalText': u'Got',
                 'pos': u'V'},
                {'index': 14, 'word': u'Cliff', 'originalText': u'Cliff',
                 'pos': u'^'},
                {'index': 15, 'word': u'Lee', 'originalText': u'Lee',
                 'pos': u'^'},
                {'index': 16, 'word': u'today', 'originalText': u'today',
                 'pos': u'N'},
                {'index': 17, 'word': u',', 'originalText': u',', 'pos': u','},
                {'index': 18, 'word': u'so', 'originalText': u'so',
                 'pos': u'P'},
                {'index': 19, 'word': u'if', 'originalText': u'if',
                 'pos': u'P'},
                {'index': 20, 'word': u'he', 'originalText': u'he',
                 'pos': u'O'},
                {'index': 21, 'word': u'loses', 'originalText': u'loses',
                 'pos': u'V'},
                {'index': 22, 'word': u'its', 'originalText': u'its',
                 'pos': u'L'},
                {'index': 23, 'word': u'on', 'originalText': u'on',
                 'pos': u'P'},
                {'index': 24, 'word': u'me', 'originalText': u'me',
                 'pos': u'O'},
                {'index': 25, 'word': u'RT', 'originalText': u'RT',
                 'pos': u'~'},
                {'index': 26, 'word': u'@e_one', 'originalText': u'@e_one',
                 'pos': u'@'},
                {'index': 27, 'word': u':', 'originalText': u':', 'pos': u'~'},
                {'index': 28, 'word': u'Texas', 'originalText': u'Texas',
                 'pos': u'^'},
                {'index': 29, 'word': u'(', 'originalText': u'(', 'pos': u','},
                {'index': 30, 'word': u'cont', 'originalText': u'cont',
                 'pos': u'~'},
                {'index': 31, 'word': u')', 'originalText': u')', 'pos': u','},
                {'index': 32, 'word': u'http://tl.gd/6meogh',
                 'originalText': u'http://tl.gd/6meogh', 'pos': u'U'}]
    tokens_1 = [{'index': 1, 'word': u'Wednesday',
                 'originalText': u'Wednesday', 'pos': u'^'},
                {'index': 2, 'word': u'27th', 'originalText': u'27th',
                 'pos': u'A'},
                {'index': 3, 'word': u'october', 'originalText': u'october',
                 'pos': u'^'},
                {'index': 4, 'word': u'2010', 'originalText': u'2010',
                 'pos': u'$'},
                {'index': 5, 'word': u'.', 'originalText': u'.', 'pos': u','},
                {'index': 6, 'word': u'》have', 'originalText': u'》have',
                 'pos': u'V'},
                {'index': 7, 'word': u'a', 'originalText': u'a', 'pos': u'D'},
                {'index': 8, 'word': u'nice', 'originalText': u'nice',
                 'pos': u'A'},
                {'index': 9, 'word': u'day', 'originalText': u'day',
                 'pos': u'N'},
                {'index': 10, 'word': u':)', 'originalText': u':)',
                 'pos': u'E'}]
    tokens_2 = [{'index': 1, 'word': u'RT',
                 'originalText': u'RT', 'pos': u'~'},
                {'index': 2, 'word': u'@DjBlack_Pearl',
                 'originalText': u'@DjBlack_Pearl', 'pos': u'@'},
                {'index': 3, 'word': u':', 'originalText': u':', 'pos': u'~'},
                {'index': 4, 'word': u'wat', 'originalText': u'wat',
                 'pos': u'O'},
                {'index': 5, 'word': u'muhfuckaz',
                 'originalText': u'muhfuckaz', 'pos': u'N'},
                {'index': 6, 'word': u'wearin', 'originalText': u'wearin',
                 'pos': u'V'},
                {'index': 7, 'word': u'4', 'originalText': u'4', 'pos': u'P'},
                {'index': 8, 'word': u'the', 'originalText': u'the',
                 'pos': u'D'},
                {'index': 9, 'word': u'lingerie', 'originalText': u'lingerie',
                 'pos': u'N'},
                {'index': 10, 'word': u'party', 'originalText': u'party',
                 'pos': u'N'},
                {'index': 11, 'word': u'?????', 'originalText': u'?????',
                 'pos': u','}]
    b_dep_0 = [{'dep': u'_', 'governor': 2, 'governorGloss': u'predict',
                'dependent': 1, 'dependentGloss': u'I'},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
                'dependent': 2, 'dependentGloss': u'predict'},
               {'dep': u'_', 'governor': 4, 'governorGloss': u"won't",
                'dependent': 3, 'dependentGloss': u'I'},
               {'dep': u'_', 'governor': 2, 'governorGloss': u'predict',
                'dependent': 4, 'dependentGloss': u"won't"},
               {'dep': u'_', 'governor': 4, 'governorGloss': u"won't",
                'dependent': 5, 'dependentGloss': u'win'},
               {'dep': u'_', 'governor': 8, 'governorGloss': u"game",
                'dependent': 6, 'dependentGloss': u'a'},
               {'dep': u'_', 'governor': 8, 'governorGloss': u"game",
                'dependent': 7, 'dependentGloss': u'single'},
               {'dep': u'_', 'governor': 5, 'governorGloss': u"win",
                'dependent': 8, 'dependentGloss': u'game'},
               {'dep': u'_', 'governor': 10, 'governorGloss': u"bet",
                'dependent': 9, 'dependentGloss': u'I'},
               {'dep': u'_', 'governor': 8, 'governorGloss': u"game",
                'dependent': 10, 'dependentGloss': u'bet'},
               {'dep': u'MWE', 'governor': 10, 'governorGloss': u"bet",
                'dependent': 11, 'dependentGloss': u'on'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 12, 'dependentGloss': u'.'},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': "ROOT",
                'dependent': 13, 'dependentGloss': u'Got'},
               {'dep': u'MWE', 'governor': 15, 'governorGloss': u"Lee",
                'dependent': 14, 'dependentGloss': u'Cliff'},
               {'dep': u'_', 'governor': 13, 'governorGloss': u"Got",
                'dependent': 15, 'dependentGloss': u'Lee'},
               {'dep': u'_', 'governor': 13, 'governorGloss': u"Got",
                'dependent': 16, 'dependentGloss': u'today'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 17, 'dependentGloss': u','},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': "ROOT",
                'dependent': 18, 'dependentGloss': u'so'},
               {'dep': u'_', 'governor': 22, 'governorGloss': u"its",
                'dependent': 19, 'dependentGloss': u'if'},
               {'dep': u'_', 'governor': 21, 'governorGloss': u"loses",
                'dependent': 20, 'dependentGloss': u'he'},
               {'dep': u'_', 'governor': 19, 'governorGloss': u"if",
                'dependent': 21, 'dependentGloss': u'loses'},
               {'dep': u'_', 'governor': 18, 'governorGloss': u"so",
                'dependent': 22, 'dependentGloss': u'its'},
               {'dep': u'_', 'governor': 22, 'governorGloss': u"its",
                'dependent': 23, 'dependentGloss': u'on'},
               {'dep': u'_', 'governor': 23, 'governorGloss': u"on",
                'dependent': 24, 'dependentGloss': u'me'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 25, 'dependentGloss': u'RT'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 26, 'dependentGloss': u'@e_one'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 27, 'dependentGloss': u':'},
               {'dep': u'_', 'governor': 21, 'governorGloss': u"loses",
                'dependent': 28, 'dependentGloss': u'Texas'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 29, 'dependentGloss': u'('},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 30, 'dependentGloss': u'cont'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 31, 'dependentGloss': u')'},
               {'dep': u'_', 'governor': -1, 'governorGloss': "$$NAN$$",
                'dependent': 32, 'dependentGloss': u'http://tl.gd/6meogh'}]
    b_dep_1 = [{'dep': u'MWE', 'governor': 2, 'governorGloss': u'27th',
                'dependent': 1, 'dependentGloss': u'Wednesday'},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
                'dependent': 2, 'dependentGloss': u'27th'},
               {'dep': u'MWE', 'governor': 1, 'governorGloss': u'Wednesday',
                'dependent': 3, 'dependentGloss': u'october'},
               {'dep': u'MWE', 'governor': 3, 'governorGloss': u'october',
                'dependent': 4, 'dependentGloss': u'2010'},
               {'dep': u'_', 'governor': -1, 'governorGloss': '$$NAN$$',
                'dependent': 5, 'dependentGloss': u'.'},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
                'dependent': 6, 'dependentGloss': u'》have'},
               {'dep': u'_', 'governor': 9, 'governorGloss': u'day',
                'dependent': 7, 'dependentGloss': u'a'},
               {'dep': u'_', 'governor': 9, 'governorGloss': u'day',
                'dependent': 8, 'dependentGloss': u'nice'},
               {'dep': u'_', 'governor': 6, 'governorGloss': u'》have',
                'dependent': 9, 'dependentGloss': u'day'},
               {'dep': u'_', 'governor': -1, 'governorGloss': '$$NAN$$',
                'dependent': 10, 'dependentGloss': u':)'}]
    b_dep_2 = [{'dep': u'_', 'governor': -1, 'governorGloss': '$$NAN$$',
                'dependent': 1, 'dependentGloss': u'RT'},
               {'dep': u'_', 'governor': -1, 'governorGloss': '$$NAN$$',
                'dependent': 2, 'dependentGloss': u'@DjBlack_Pearl'},
               {'dep': u'_', 'governor': -1, 'governorGloss': u'$$NAN$$',
                'dependent': 3, 'dependentGloss': u':'},
               {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
                'dependent': 4, 'dependentGloss': u'wat'},
               {'dep': u'_', 'governor': 6, 'governorGloss': u'wearin',
                'dependent': 5, 'dependentGloss': u'muhfuckaz'},
               {'dep': u'_', 'governor': 4, 'governorGloss': u'wat',
                'dependent': 6, 'dependentGloss': u'wearin'},
               {'dep': u'_', 'governor': 6, 'governorGloss': u'wearin',
                'dependent': 7, 'dependentGloss': u'4'},
               {'dep': u'_', 'governor': 10, 'governorGloss': u'party',
                'dependent': 8, 'dependentGloss': u'the'},
               {'dep': u'_', 'governor': 10, 'governorGloss': u'party',
                'dependent': 9, 'dependentGloss': u'lingerie'},
               {'dep': u'_', 'governor': 7, 'governorGloss': u'4',
                'dependent': 10, 'dependentGloss': u'party'},
               {'dep': u'_', 'governor': -1, 'governorGloss': '$$NAN$$',
                'dependent': 11, 'dependentGloss': u'?????'}]

    test_sentences = [u"I predict I won't win a single game I bet on. "
                      u"Got Cliff Lee today, so if he loses its on me RT "
                      u"@e_one: Texas (cont) http://tl.gd/6meogh",
                      u"Wednesday 27th october 2010. 》have a nice day :)"]
    expected_return = [{'index': 0,
                        'basicDependencies': b_dep_0, 'tokens': tokens_0},
                       {'index': 1,
                        'basicDependencies': b_dep_1, 'tokens': tokens_1}]
    assert expected_return == tweebo.process_texts(test_sentences,
                                                   output_type='stanford')

    test_sentences = ["I predict I won't win a single game I bet on. "
                      "Got Cliff Lee today, so if he loses its on me RT "
                      "@e_one: Texas (cont) http://tl.gd/6meogh",
                      "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                      "party?????"]
    expected_return = [{'index': 0,
                        'basicDependencies': b_dep_0, 'tokens': tokens_0},
                       {'index': 1,
                        'basicDependencies': b_dep_2, 'tokens': tokens_2}]
    assert expected_return == tweebo.process_texts(test_sentences,
                                                   output_type='stanford')

    expected_return = [{'index': 0,
                        'basicDependencies': [], 'tokens': []},
                       {'index': 1,
                        'basicDependencies': [], 'tokens': []}]
    assert expected_return == tweebo.process_texts(['', ''],
                                                   output_type='stanford')

    test_sentences = ["I predict I won't win a single game I bet on. "
                      "Got Cliff Lee today, so if he loses its on me RT "
                      "@e_one: Texas (cont) http://tl.gd/6meogh",
                      "              ",
                      "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                      "party?????"]
    expected_return = [{'index': 0,
                        'basicDependencies': b_dep_0, 'tokens': tokens_0},
                       {'index': 1, 'basicDependencies': [], 'tokens': []},
                       {'index': 2,
                        'basicDependencies': b_dep_2, 'tokens': tokens_2}]
    assert expected_return == tweebo.process_texts(test_sentences,
                                                   output_type='stanford')


def test_process_texts_conll():
    '''
    Tests :py:func:`tweebo.process_texts` where the output type is conll. \
    We perform the following tests:
    1. 2 unicode sentences
    2. 2 ASCII sentences
    3. 3 ASCII sentences where the 2nd sentence is empty.
    '''

    conll_0 = (u'1\tI\t_\tO\tO\t_\t2\t_\n'
               u'2\tpredict\t_\tV\tV\t_\t0\t_\n'
               u'3\tI\t_\tO\tO\t_\t4\t_\n'
               u"4\twon't\t_\tV\tV\t_\t2\t_\n"
               u'5\twin\t_\tV\tV\t_\t4\t_\n'
               u'6\ta\t_\tD\tD\t_\t8\t_\n'
               u'7\tsingle\t_\tA\tA\t_\t8\t_\n'
               u'8\tgame\t_\tN\tN\t_\t5\t_\n'
               u'9\tI\t_\tO\tO\t_\t10\t_\n'
               u'10\tbet\t_\tV\tV\t_\t8\t_\n'
               u'11\ton\t_\tP\tP\t_\t10\tMWE\n'
               u'12\t.\t_\t,\t,\t_\t-1\t_\n'
               u'13\tGot\t_\tV\tV\t_\t0\t_\n'
               u'14\tCliff\t_\t^\t^\t_\t15\tMWE\n'
               u'15\tLee\t_\t^\t^\t_\t13\t_\n'
               u'16\ttoday\t_\tN\tN\t_\t13\t_\n'
               u'17\t,\t_\t,\t,\t_\t-1\t_\n'
               u'18\tso\t_\tP\tP\t_\t0\t_\n'
               u'19\tif\t_\tP\tP\t_\t22\t_\n'
               u'20\the\t_\tO\tO\t_\t21\t_\n'
               u'21\tloses\t_\tV\tV\t_\t19\t_\n'
               u'22\tits\t_\tL\tL\t_\t18\t_\n'
               u'23\ton\t_\tP\tP\t_\t22\t_\n'
               u'24\tme\t_\tO\tO\t_\t23\t_\n'
               u'25\tRT\t_\t~\t~\t_\t-1\t_\n'
               u'26\t@e_one\t_\t@\t@\t_\t-1\t_\n'
               u'27\t:\t_\t~\t~\t_\t-1\t_\n'
               u'28\tTexas\t_\t^\t^\t_\t21\t_\n'
               u'29\t(\t_\t,\t,\t_\t-1\t_\n'
               u'30\tcont\t_\t~\t~\t_\t-1\t_\n'
               u'31\t)\t_\t,\t,\t_\t-1\t_\n'
               u'32\thttp://tl.gd/6meogh\t_\tU\tU\t_\t-1\t_')
    conll_1 = (u'1\tWednesday\t_\t^\t^\t_\t2\tMWE\n'
               u'2\t27th\t_\tA\tA\t_\t0\t_\n'
               u'3\toctober\t_\t^\t^\t_\t1\tMWE\n'
               u"4\t2010\t_\t$\t$\t_\t3\tMWE\n"
               u'5\t.\t_\t,\t,\t_\t-1\t_\n'
               u'6\t》have\t_\tV\tV\t_\t0\t_\n'
               u'7\ta\t_\tD\tD\t_\t9\t_\n'
               u'8\tnice\t_\tA\tA\t_\t9\t_\n'
               u'9\tday\t_\tN\tN\t_\t6\t_\n'
               u'10\t:)\t_\tE\tE\t_\t-1\t_')
    conll_2 = (u'1\tRT\t_\t~\t~\t_\t-1\t_\n'
               u'2\t@DjBlack_Pearl\t_\t@\t@\t_\t-1\t_\n'
               u'3\t:\t_\t~\t~\t_\t-1\t_\n'
               u"4\twat\t_\tO\tO\t_\t0\t_\n"
               u'5\tmuhfuckaz\t_\tN\tN\t_\t6\t_\n'
               u'6\twearin\t_\tV\tV\t_\t4\t_\n'
               u'7\t4\t_\tP\tP\t_\t6\t_\n'
               u'8\tthe\t_\tD\tD\t_\t10\t_\n'
               u'9\tlingerie\t_\tN\tN\t_\t10\t_\n'
               u'10\tparty\t_\tN\tN\t_\t7\t_\n'
               u'11\t?????\t_\t,\t,\t_\t-1\t_')

    test_sentences = [u"I predict I won't win a single game I bet on. "
                      u"Got Cliff Lee today, so if he loses its on me RT "
                      u"@e_one: Texas (cont) http://tl.gd/6meogh",
                      u"Wednesday 27th october 2010. 》have a nice day :)"]
    expected_return = [conll_0, conll_1]
    assert expected_return == tweebo.process_texts(test_sentences)

    test_sentences = ["I predict I won't win a single game I bet on. "
                      "Got Cliff Lee today, so if he loses its on me RT "
                      "@e_one: Texas (cont) http://tl.gd/6meogh",
                      "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                      "party?????"]
    expected_return = [conll_0, conll_2]
    assert expected_return == tweebo.process_texts(test_sentences,
                                                   output_type='conll')

    assert tweebo.process_texts(['', '']) == ['', '']

    test_sentences = ["I predict I won't win a single game I bet on. "
                      "Got Cliff Lee today, so if he loses its on me RT "
                      "@e_one: Texas (cont) http://tl.gd/6meogh",
                      "              ",
                      "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                      "party?????"]
    expected_return = [conll_0, '', conll_2]
    assert expected_return == tweebo.process_texts(test_sentences)


def test_process_texts_exceptions():
    '''
    Tests the different excpetions that should be raises by the process_texts \
    method.
    1. ValueError: This should be raised when the output_type is not \
    `stanford` or `conll`
    2. TypeError: This should be raised as the texts input is not a list.
    3. TypeError: This should be raises as the texts input is a list of ints \
    not a list of Strings.
    '''

    test_sentence = ["Some text to process"]
    with pytest.raises(ValueError):
        tweebo.process_texts(test_sentence, output_type='not correct')
    with pytest.raises(TypeError):
        tweebo.process_texts('some text to process')
    with pytest.raises(TypeError):
        tweebo.process_texts([1, 2])
