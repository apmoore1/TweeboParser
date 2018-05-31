'''
Contains the following test functions:
1. test_get_sha_digest -- Tests that the method used to get an SHA-1 digest \
works correctly by testing it on different and same files.
2. test_output -- Tests if the output of the new code base is the same as \
a stable code commit.
'''

import logging
import threading
from pathlib import Path
import tempfile
from traceback import format_exc
import subprocess
import shutil
import sha

import pytest


def _get_sha_digest(file_path):
    '''
    :param file_path: Path to the file you want to get an SHA-1 digest \
    from the content of the file.
    :type file_path: Path
    :return: SHA-1 digest of the content within the file at file_path
    :rtype: str
    '''

    file_hash = sha.new()
    with file_path.open('r', encoding='utf-8') as lines:
        for line in lines:
            file_hash.update(line.encode('utf-8'))
    return file_hash.digest()


def _detailed_comparison(test_fp, gold_fp):
    '''
    Ensures that each line in the test_fp file is the same as the lines in \
    the gold_fp file.

    :param test_fp: File path to a test file
    :param gold_fp: File path to the gold standard file
    :type test_fp: Path
    :type gold_fp: Path
    :return: None
    :rtype: None
    :raises Exception: If there is a line in the test_fp that is not the same \
    as the corresponding line in the gold_fp file.
    '''

    test_lines = list(test_fp.open('r', encoding='utf-8'))
    gold_lines = list(gold_fp.open('r', encoding='utf-8'))

    for index, gold_line in enumerate(gold_lines):
        test_line = test_lines[index].strip()
        gold_line = gold_line.strip()

        if gold_line != test_line:
            raise Exception('Test and Gold data not the same at line {}'
                            '\nTest has following text: {}\n'
                            'Gold has: {}'.format(index, test_line, gold_line))


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


def test_detailed_comparison():
    '''
    Tests if the _detailed_comparison method works correctly. The method \
    should raise an Exception when the two files are not the same. Should \
    return None when the files are the same.

    Tests:
    1. Return None when the test file is sherlock_holmes_text_only_copy.txt \
    and the gold file is sherlock_holmes_text_only.txt
    2. Raise an Exception when the test file is sherlock_holmes.txt and the \
    gold file is sherlock_holmes_text_only.txt
    '''

    this_dir = Path(__file__).absolute().parent.resolve()
    sherlock_text_only = Path(this_dir, 'test_data',
                              'sherlock_holmes_text_only.txt')
    sherlock_text_only_copy = Path(this_dir, 'test_data',
                                   'sherlock_holmes_text_only_copy.txt')
    _detailed_comparison(sherlock_text_only_copy, sherlock_text_only)

    sherlock_original = Path(this_dir, 'test_data',
                             'sherlock_holmes.txt')
    with pytest.raises(Exception):
        _detailed_comparison(sherlock_original, sherlock_text_only)


def test_get_sha_digest():
    '''
    Tests if the _get_sha_digest method works correctly. The method returns \
    an SHA-1 digest from the contents of the file path it was given.

    Tests:
    1. The copy of the text only sherlock holmes should have the same digest \
    as the original it was copied from.
    2. The sherlock holmes with the whitespace removed should have a \
    different digest to that of the one with the whitespace still their.
    '''

    this_dir = Path(__file__).absolute().parent.resolve()
    sherlock_fp = Path(this_dir, 'test_data', 'sherlock_holmes_text_only.txt')
    sherlock_copy_fp = Path(this_dir, 'test_data',
                            'sherlock_holmes_text_only_copy.txt')
    sherlock_digest = _get_sha_digest(sherlock_fp)
    sherlock_copy_digest = _get_sha_digest(sherlock_copy_fp)
    assert sherlock_digest == sherlock_copy_digest

    sherlock_diff_fp = Path(this_dir, 'test_data', 'sherlock_holmes.txt')
    sherlock_diff_digest = _get_sha_digest(sherlock_diff_fp)
    assert sherlock_digest != sherlock_diff_digest


def test_output():
    '''
    Tests if the new version of the code still outputs the same parse result.

    We test this by having output from the TweeboParser from the following \
    commit version:`e923216e4141610e40cc5c6712970a1afcc9c400
    <https://github.com/apmoore1/TweeboParser/tree\
    /e923216e4141610e40cc5c6712970a1afcc9c400>`_ \
    on the Sherlock Holmes data and compare it to the new code parse of this \
    data. We compare using SHA-1 digests, if they have the same digest then \
    the test pass.

    To be done: 1. Better error messages for failed test case. e.g. which \
    lines of the Sherlock holmes text the parser failed on.
    '''

    this_dir = Path(__file__).absolute().parent.resolve()
    tweets_fp = this_dir.joinpath('test_data', 'tweets.txt')
    gold_test_fp = this_dir.joinpath('test_data',
                                     'tweets.txt.predict')
    gold_test_digest = _get_sha_digest(gold_test_fp)

    temp_dir_fp = tempfile.mkdtemp()
    try:
        text_fp = Path(temp_dir_fp, 'text_file.txt')
        result_fp = Path(temp_dir_fp, 'text_file.txt.predict')
        shutil.copyfile(str(tweets_fp),
                        str(text_fp))
        _process_file(text_fp)
        result_digest = _get_sha_digest(result_fp)
        _detailed_comparison(result_fp, gold_test_fp)
        assert result_digest == gold_test_digest

    except Exception as e:
        shutil.rmtree(temp_dir_fp)
        print('Error {} during running the Tweebo run script, '
              'Stack Trace:\n {}'.format(repr(e), format_exc()))
    else:
        shutil.rmtree(temp_dir_fp)


def test_multi_threading_output():
    '''
    This checks that the run.sh script can be run on different threads. This \
    is done by creating two threads and running two different files on the \
    run script at the same time using the two threads. We then test to \
    ensure the output file exists for each of the two inputted file exists \
    and contains come content.
    '''

    logging.basicConfig(level=logging.WARNING,
                        format='(%(threadName)-10s) %(message)s')
    this_dir = Path(__file__).absolute().parent.resolve()
    sherlock_fp_1 = this_dir.joinpath('test_data1',
                                      'sherlock_holmes_text_only.txt')
    sherlock_fp_2 = this_dir.joinpath('test_data2',
                                      'sherlock_holmes_text_only.txt')
    files_to_process = [sherlock_fp_1, sherlock_fp_2]
    threads = []
    for file_to_process in files_to_process:
        thread = threading.Thread(target=_process_file,
                                  args=(file_to_process,))
        thread.setDaemon(True)
        threads.append(thread)
        thread.start()
        logging.warning('starting %s processing %s',
                        thread.getName(), str(file_to_process))
    for thread in threads:
        thread.join()
        logging.warning('joining %s', thread.getName())
    for thread in threads:
        if thread.isAlive():
            raise Exception('Thread {} is still alive'
                            .format(thread.getName()))
    sherlock_result_fp_1 = this_dir.joinpath('test_data1',
                                             'sherlock_holmes_text_only'
                                             '.txt.predict')
    sherlock_result_fp_2 = this_dir.joinpath('test_data2',
                                             'sherlock_holmes_text_only'
                                             '.txt.predict')
    result_files = [sherlock_result_fp_1, sherlock_result_fp_2]
    for result_file in result_files:
        assert result_file.is_file()
        assert result_file.stat().st_size > 1000
