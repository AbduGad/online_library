import sys
import os
set_testEnv = os.environ['test_db'] = 'true'
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
set_parent_dir = sys.path.append(parent_dir)
