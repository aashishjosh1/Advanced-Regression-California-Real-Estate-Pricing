#! /usr/bin/python

import sys
sys.path.insert(0, "/var/www/analysis_and_prediction_of_house_prices")
sys.path.insert(0,'/opt/conda/lib/python3.6/site-packages')
sys.path.insert(0, "/opt/conda/bin/")
    
import os
os.environ['PYTHONPATH'] = '/opt/conda/bin/python'

from source_code.analysis_and_prediction_of_house_prices import app as application