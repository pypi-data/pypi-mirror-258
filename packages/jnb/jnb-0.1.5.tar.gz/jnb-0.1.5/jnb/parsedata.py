import argparse


class ParseData:
    def __init__(self):
        pass

    def ffooo(self):
        pass

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(prog='JNB')
        parser.add_argument('-c', '--create',
                            action='extend',
                            help='New Jupyter Notebooks to be created',
                            nargs='+',
                            type=str,
                            required=True)
        return parser

    @staticmethod
    def parse_data():
        parser = ParseData.get_parser()
        args = parser.parse_args()
        return args
