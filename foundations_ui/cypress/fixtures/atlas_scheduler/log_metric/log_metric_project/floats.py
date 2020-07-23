import foundations
import numpy as np
from time import sleep

foundations.log_metric("metric_float", 1.)
foundations.log_metric("metric_large_float", 999999999.8888888888888888)
foundations.log_metric("metric_list_of_floats", [1., 2.])
foundations.log_metric("metric_long_list_of_floats", [1., 2., 1., 2., 1., 2., 1., 2., 1., 2., 1., 2., 1., 2., 1., 2., 1., 2., 1., 2., ])
foundations.log_metric("metric_long_list_of_long_floats", [999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888,
                                                    999999999.8888888888888888])

foundations.log_metric("metric_mixed_type", 2.222)

numpy_value = np.float64(5)
foundations.log_metric("numpy_value", numpy_value)

for i in range(20):
  foundations.log_metric("metric_repeat", i/3.)
  sleep(.1)
