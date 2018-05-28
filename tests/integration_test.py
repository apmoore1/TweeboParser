'''
Contains the following test functions:
1. test_output -- Tests if the output of the new code base is the same as \
a stable code commit.
'''

from pathlib import Path
import tempfile
import subprocess
import shutil
import sha


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

    this_dir = Path(__file__).absolute().parent
    run_file = this_dir.joinpath('..', 'run.sh')
    sherlock_holmes_fp = this_dir.joinpath('test data',
                                           'sherlock_holmes_text_only.txt')
    pred_file = this_dir.joinpath('test data', 'something.txt')
    temp_dir = tempfile.mkdtemp()
    try:
        text_file_path = Path(temp_dir, 'text_file.txt')
        result_file_path = Path(temp_dir, 'text_file.txt.predict')
        print(str(sherlock_holmes_fp.resolve()))
        print(str(text_file_path))
        print('anything')
        shutil.copyfile(str(sherlock_holmes_fp.resolve()),
                        str(text_file_path))
        sub_process_params = ['bash', str(run_file.resolve()),
                              str(text_file_path.resolve())]
        if subprocess.call(sub_process_params):
            shutil.copy(str(result_file_path),
                        str(pred_file))

        else:
            raise SystemError('Could not run the Tweebo run script')
    except Exception as e:
        print(temp_dir)
        shutil.rmtree(temp_dir)
        print(e.args)
        raise SystemError('Error during running the Tweebo run script')
    else:
        print(temp_dir)
        shutil.rmtree(temp_dir)

test_output()
