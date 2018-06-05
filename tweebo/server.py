# encoding: utf-8
'''
Flask API for the TweeboParser.
'''

import argparse
import logging
import multiprocessing

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from marshmallow import Schema, fields, ValidationError
from waitress import serve

from tweebo import process_texts


app = Flask(__name__)
api = Api(app)


class InputSchema(Schema):
    def valid_output_types(output_type):
        output_types_allowed = ['conll', 'stanford']
        if output_type.lower() not in output_types_allowed:
            raise ValidationError('output_type should be one of these '
                                  'values {}'.format(output_types_allowed))

    output_type = fields.String(required=True, validate=valid_output_types)
    texts = fields.List(fields.String(), required=True)


class ConllSchema(Schema):
    data = fields.List(fields.String, required=True)


class StanfordSchema(Schema):
    data = fields.List(fields.Dict(keys=fields.String), required=True)


input_schema = InputSchema()
conll_schema = ConllSchema()
stanford_schema = StanfordSchema()


class TweeboParser(Resource):
    def post(self):
        input_data = request.get_json()
        if not input_data:
            abort(400,
                  message='No input data. Expect output_type and texts inputs')
        input_val_errors = input_schema.validate(request.get_json())
        if input_val_errors:
            abort(422, message='{}'.format(input_val_errors))
        try:
            processed_texts = process_texts(**input_data)
        except Exception as exception:
            abort(415, message='Error: {}'.format(repr(exception)))
        output_type = input_data['output_type'].lower()
        process_val_errors = None
        if output_type == 'conll':
            process_val_errors = conll_schema.validate({'data':
                                                        processed_texts})
        else:
            process_val_errors = stanford_schema.validate({'data':
                                                          processed_texts})
        if process_val_errors:
            abort(422, message='{}'.format(process_val_errors))
        return jsonify(processed_texts)


api.add_resource(TweeboParser, '/')

description = 'Starts the API server for TweeboParser'
parser = argparse.ArgumentParser(prog='TweeboParser Server',
                                 description=description)
threads_help = 'The number of threads the server will use (default: number '\
               'of threads equal to number of CPUs)'
parser.add_argument('-t', '--threads', type=int,
                    help=threads_help, default=multiprocessing.cpu_count())
port_help = 'Port number to run the server from (default: 8000)'
parser.add_argument('-p', '--port', type=int,
                    help=port_help, default=8000)
hostname_help = 'Hostname/IP address on which the server listen to '\
                '(default: 0.0.0.0)'
parser.add_argument('--hostname', type=str,
                    help=hostname_help, default='0.0.0.0')

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.INFO)

    args = parser.parse_args()
    logging.info('Serving on: {}:{}'.format(args.hostname, args.port))
    logging.info('Number of threads allocated: {}'.format(args.threads))
    serve(app, host=args.hostname, port=args.port,
          threads=args.threads)
