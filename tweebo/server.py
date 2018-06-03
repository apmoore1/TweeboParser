# encoding: utf-8
'''
Flask API for the TweeboParser.
'''

from flask import Flask
from flask_restful import Resource, Api, reqparse
from marshmallow import Schema, fields

from tweebo import process_texts


app = Flask(__name__)
api = Api(app)


class Data(Schema):
    output_type = fields.Str()
    texts = fields.List()


parser = reqparse.RequestParser()
parser.add_argument('output_type', type=str, choices=('conll', 'stanford'),
                    help='The type of output either `conll` or `stanford`')
parser.add_argument('texts', type=str, action='append',
                    help='List of texts that are to be processed')


class TweeboParser(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        processed_texts = process_texts(**args)
        return processed_texts


api.add_resource(TweeboParser, '/')

if __name__ == '__main__':
    app.run(debug=True)
