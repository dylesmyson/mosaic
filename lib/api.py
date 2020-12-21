import yaml
import logging

from lib.session import Session
from lib.generator import Generators


# logging.basicConfig(level='INFO')
logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)


class ApiV1:
    @staticmethod
    def connect(args):
        """ docstring
        """

        logger.debug(f"Calling connect with {args}")

        session = Session(args.name)

    @staticmethod
    def play(args):
        """ docstring
        """

        logger.debug(f"Calling play with {args}")

        session = Session('mosaic')
        session.load(args.filepath)
        session.play()

    @staticmethod
    def generate(args):
        """ docstring
        """

        logger.debug(f"Calling generate with {args}")

        with open(args.filepath, 'r') as yaml_conf:
            conf = yaml.safe_load(yaml_conf)

        algorithm = getattr(Generators, conf['algorithm'])
        algorithm(conf)


class Api(ApiV1):
    pass
