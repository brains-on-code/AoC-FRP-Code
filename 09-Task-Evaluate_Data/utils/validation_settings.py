import re

START_TARGET_POSITION = 'Target Position Results'
END_TARGET_POSITION = 'Done Target Position Results '

COLUMN_KEY = 'key'
COLUMN_VALUE = 'value'
COLUMN_INDEX = 'index'

HEAD_INDEX = -1

ARRAY_LIST_PATTERN = re.compile(r'(\d|\.) +,? *')
