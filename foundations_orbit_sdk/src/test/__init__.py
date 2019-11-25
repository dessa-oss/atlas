"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import coverage

cov = coverage.Coverage()
cov.start()

from .contract_validators import *

from .test_track_production_metrics import TestTrackProductionMetrics
from .test_data_contract import TestDataContract
from .test_data_contract_options import TestDataContractOptions
from .test_report_formatter import TestReportFormatter
from .test_data_contract_summary import TestDataContractSummary
from .test_data_contract_categorizer import TestDataContractCategorizer

cov.stop()
cov.save()

cov.html_report(directory='../../coverage_results/foundations_orbit_sdk')
