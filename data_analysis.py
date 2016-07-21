# ///////////////////////////////////////
# /*                                   */
# /*           Data Analysis           */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*                                   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime, timedelta
import copy

class DataProcessing(object):

	def __init__(self, raw=True):
		super(DataProcessing, self).__init__()
		self.raw = raw

	def raw_analysis(self):
		pass

	def synthetic_analysis(self):
		pass

	def analysis(self):
		pass