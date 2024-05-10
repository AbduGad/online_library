import sys
import os
set_testEnv = os.environ['test_db'] = 'true'
print(sys.path)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
