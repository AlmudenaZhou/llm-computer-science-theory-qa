import os
import sys
import logging
import logging.config
from dotenv import load_dotenv

sys.path.append(os.getcwd())

logging.config.fileConfig('logger.conf')
logger = logging.getLogger(__name__)

from src.indexing.preprocessing_workflow import preprocessing_workflow
from src.indexing.indexing_documents import indexing_workflow


load_dotenv()


def main():

    preprocessing_workflow()
    indexing_workflow()


if __name__ == "__main__":
    main()