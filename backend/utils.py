from flask_restful import reqparse

def gen_fields(parser, fields):
    for field in fields:
        parser.add_argument(field)
    return parser.parse_args()