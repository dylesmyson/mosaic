import yaml
from lib.session import Session
from lib.generator import Generators


class ApiV1:
    @staticmethod
    def connect(args):
        """ docstring
        """
        session = Session(args.name)
        print('Session connected!')
        print('Call `help(session)` for help.')

    @staticmethod
    def play(args):
        """ docstring
        """
        session = Session('mosaic')
        session.load(args.filepath)
        session.play()

    @staticmethod
    def generate(args):
        """ docstring
        """
        with open(args.filepath, 'r') as yaml_conf:
            conf = yaml.safe_load(yaml_conf)

        algorithm = getattr(Generators, conf['algorithm'])
        algorithm(conf)


class Api(ApiV1):
    pass
