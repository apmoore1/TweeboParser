'''
Contains the following test functions:
1. test_get_sha_digest -- Tests that the method used to get an SHA-1 digest \
works correctly by testing it on different and same files.
2. test_output -- Tests if the output of the new code base is the same as \
a stable code commit.
'''

from pathlib import Path
import tempfile
import subprocess
import shutil
import sha


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
    sherlock_fp = Path(this_dir, 'test data', 'sherlock_holmes_text_only.txt')
    sherlock_copy_fp = Path(this_dir, 'test data',
                            'sherlock_holmes_text_only_copy.txt')
    sherlock_digest = _get_sha_digest(sherlock_fp)
    sherlock_copy_digest = _get_sha_digest(sherlock_copy_fp)
    assert sherlock_digest == sherlock_copy_digest

    sherlock_diff_fp = Path(this_dir, 'test data', 'sherlock_holmes.txt')
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
    run_file = this_dir.joinpath('..', 'run.sh').resolve()
    sherlock_holmes_fp = this_dir.joinpath('test data',
                                           'sherlock_holmes_text_only.txt')
    gold_test_fp = this_dir.joinpath('test data',
                                     'sherlock_holmes_text_only.txt.predict')
    gold_test_digest = _get_sha_digest(gold_test_fp)

    temp_dir_fp = tempfile.mkdtemp()
    try:
        text_fp = Path(temp_dir_fp, 'text_file.txt')
        result_fp = Path(temp_dir_fp, 'text_file.txt.predict')
        shutil.copyfile(str(sherlock_holmes_fp),
                        str(text_fp))
        sub_process_params = ['bash', str(run_file),
                              str(text_fp)]
        if subprocess.call(sub_process_params):
            raise SystemError('Could not run the Tweebo run script')
        result_digest = _get_sha_digest(result_fp)
        assert result_digest == gold_test_digest

    except Exception as e:
        shutil.rmtree(temp_dir_fp)
        print(e.args)
        raise SystemError('Error during running the Tweebo run script')
    else:
        shutil.rmtree(temp_dir_fp)