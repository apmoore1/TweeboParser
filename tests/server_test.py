'''
Tests the API server in :py:mod:`tweebo.server`. \
The test functions within this module are the following:
1. test_server_conll - Ensures the API server can handle requests to process \
data and return it in the CoNLL format.
2. test_server_stanford - Ensures the API server can handle requests to \
process data and return it in the stanford format.
3. test_exceptions - Ensures the API server returns the correct HTTPError \
codes for exception cases.
4. test_multi_requests - Ensure the API server can handle multiple \
simultaneous requests.
'''

from itertools import product
import json
from multiprocessing import Process, Pool
import time

import requests
from requests.exceptions import HTTPError
from waitress import serve
import pytest

from tweebo import server
import tweebo_test


def _start_server():
    '''
    Starts the API server.
    '''

    serve(server.app, port=8000, threads=4)


def test_server_conll():
    '''
    Tests that the API server when given correct input data returns data \
    in the correct format. In this case the conll format. Follows the same \
    tests as those in :py:func:`tweebo_test.test_process_texts_conll`
    '''

    tweebo_server = Process(target=_start_server)
    tweebo_server.start()
    time.sleep(1)
    try:
        output_type = 'conll'
        texts = tweebo_test.TEST_SENTENCES_0
        test_data = {'texts': texts, 'output_type': output_type}
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        assert response.json() == [tweebo_test.CONLL_0, tweebo_test.CONLL_1]

        texts = tweebo_test.TEST_SENTENCES_1
        test_data['texts'] = texts
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        assert response.json() == [tweebo_test.CONLL_0, tweebo_test.CONLL_2]

        test_data['texts'] = ['    ', '']
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        assert response.json() == ['', '']

        texts = tweebo_test.TEST_SENTENCES_2
        test_data['texts'] = texts
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        assert response.json() == [tweebo_test.CONLL_0, '',
                                   tweebo_test.CONLL_2]
    except Exception as error:
        tweebo_server.terminate()
        raise error
    else:
        tweebo_server.terminate()


def test_server_stanford():
    '''
    Tests that the API server when given correct input data returns data \
    in the correct format. In this case the stanford format. Follows the same \
    tests as those in :py:func:`tweebo_test.test_process_texts_stanford`
    '''

    tweebo_server = Process(target=_start_server)
    tweebo_server.start()
    time.sleep(1)
    try:
        output_type = 'stanford'
        texts = tweebo_test.TEST_SENTENCES_0
        test_data = {'texts': texts, 'output_type': output_type}
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        expected_return = [{'index': 0,
                            'basicDependencies': tweebo_test.B_DEP_0,
                            'tokens': tweebo_test.TOKENS_0},
                           {'index': 1,
                            'basicDependencies': tweebo_test.B_DEP_1,
                            'tokens': tweebo_test.TOKENS_1}]
        assert response.json() == expected_return

        texts = tweebo_test.TEST_SENTENCES_1
        test_data['texts'] = texts
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        expected_return = [{'index': 0,
                            'basicDependencies': tweebo_test.B_DEP_0,
                            'tokens': tweebo_test.TOKENS_0},
                           {'index': 1,
                            'basicDependencies': tweebo_test.B_DEP_2,
                            'tokens': tweebo_test.TOKENS_2}]
        assert response.json() == expected_return

        test_data['texts'] = ['    ', '']
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        expected_return = [{'index': 0,
                            'basicDependencies': [], 'tokens': []},
                           {'index': 1,
                            'basicDependencies': [], 'tokens': []}]
        assert response.json() == expected_return

        texts = tweebo_test.TEST_SENTENCES_2
        test_data['texts'] = texts
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        expected_return = [{'index': 0,
                            'basicDependencies': tweebo_test.B_DEP_0,
                            'tokens': tweebo_test.TOKENS_0},
                           {'index': 1, 'basicDependencies': [], 'tokens': []},
                           {'index': 2,
                            'basicDependencies': tweebo_test.B_DEP_2,
                            'tokens': tweebo_test.TOKENS_2}]
        assert response.json() == expected_return
    except Exception as error:
        tweebo_server.terminate()
        raise error
    else:
        tweebo_server.terminate()


def test_exceptions():
    '''
    Test that the API server raises HTTPErrors correctly. Test cases:
    1. Raise 422 when no texts input.
    2. Raise 422 when texts contains the wrong input type.
    3. Raise 422 when no output_type input
    4. Raise 422 when output_type contain the wrong input type.
    5. Raise 422 when output_type is not `conll` or `stanford`
    6. Raise 400 when data is not json formated
    '''

    tweebo_server = Process(target=_start_server)
    tweebo_server.start()
    time.sleep(1)
    try:
        # Test 1
        output_type = 'conll'
        test_data = {'output_type': output_type}
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 422
        # Test 2
        test_data['texts'] = 'hello how are you'
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 422
        # Test 3
        test_data = {'texts': ['hello how are you']}
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 422
        # Test 4
        test_data['output_dict'] = ['conll']
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 422
        # Test 5
        test_data['output_dict'] = 'conlls'
        response = requests.post('http://127.0.0.1:8000', json=test_data)
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 422
        # Test 6
        test_data['output_dict'] = 'conll'
        response = requests.post('http://127.0.0.1:8000',
                                 data=json.dumps(test_data))
        with pytest.raises(HTTPError):
            error = response.raise_for_status()
        assert response.status_code == 400
    except Exception as error:
        tweebo_server.terminate()
        raise error
    else:
        tweebo_server.terminate()


def _api_request(data):
    response = requests.post('http://127.0.0.1:8000', json=data)
    return response.json()


def test_multi_requests():
    '''
    Test that the server API can handle multiple simultaneous requests.
    '''

    tweebo_server = Process(target=_start_server)
    tweebo_server.start()
    time.sleep(1)
    try:
        process_pool = Pool(3)
        input_text = [tweebo_test.TEST_SENTENCES_0,
                      tweebo_test.TEST_SENTENCES_1,
                      tweebo_test.TEST_SENTENCES_2]
        output_types = ['conll', 'CoNLL']
        input_data = [{'texts': texts, 'output_type': output_type}
                      for output_type, texts in
                      product(output_types, input_text)]
        output_data = None
        try:
            output_data = process_pool.map(_api_request, input_data)
        except Exception as error:
            process_pool.terminate()
            raise error
        else:
            process_pool.terminate()
        expected_return = [[tweebo_test.CONLL_0, tweebo_test.CONLL_1],
                           [tweebo_test.CONLL_0, tweebo_test.CONLL_2],
                           [tweebo_test.CONLL_0, '', tweebo_test.CONLL_2]] * 2
        assert output_data == expected_return
    except Exception as error:
        tweebo_server.terminate()
        raise error
    else:
        tweebo_server.terminate()
