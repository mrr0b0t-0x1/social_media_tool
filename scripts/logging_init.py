import sys
sys.path.append("..")

from globals import ROOT_DIR
import logging

FORMAT = '\n---------------------------------------------------------------------------------------\n%(asctime)s - %(message)s\n---------------------------------------------------------------------------------------\n'

logger_init = logging.getLogger(__name__)
fh = logging.FileHandler(filename=ROOT_DIR / 'logs' / 'app.log')
formatter = logging.Formatter(fmt=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(fmt=formatter)
fh.setLevel(logging.INFO)
logger_init.addHandler(fh)
logger_init.propagate = False


if __name__ == '__main__':
    if sys.argv[1] == '--start':
        logger_init.info("Started")
    elif sys.argv[1] == '--stop':
        logger_init.info("Stopped")
        logging.shutdown()
