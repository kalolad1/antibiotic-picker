import os

from . import path_constants

SLOW_TEST_FLAG = "slow"
FIXTURES_DIR_PATH = os.path.join(path_constants.CORE_PARENT_PATH, "fixtures")
FIXTURES = [file_name for file_name in os.listdir(FIXTURES_DIR_PATH)]
