"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This very simple module shows the lightweight syntax introduced by Foundations.
After importing Foundations, you can import the modules containing code you created
almost as usual.  The only difference is that you should prefix the module name with
"staged_".

With that "staged_" prefix, Foundations does some magic that wraps your code in layers
which perform provenance tracking, caching, prepping your job for deployment to compute, and so on.

The "main" code below is exactly what you'd write without Foundations, save for that
.run() method.  When you call .run(), the job code is packaged and sent to a configured compute -
could be GCP, your local machine, or even an NVIDIA DGX!  This configuration will be set in
a configuration yaml provided as a result of installation / integration of Foundations.  It
can also be set programmatically, as shown in the config module.

You can in principle use the .run() method on any stage, but using it on the final stage is
usually what you want.
"""

import foundations
from common.data import load_titanic
from common.prep import get_mode, fillna
from common.logging import log_data

load_titanic = foundations.create_stage(load_titanic)
get_mode = foundations.create_stage(get_mode)
fillna = foundations.create_stage(fillna)
log_data = foundations.create_stage(log_data)


if __name__ == '__main__':
    data = load_titanic()
    mode = get_mode(data, 'Cabin')
    data = fillna(data, 'Cabin', mode)
    log_data(data).run()
