import foundations
from time import sleep

foundations.log_param("param_str", str(1.))
foundations.log_param("param_long_str", "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf")
foundations.log_param("param_long_list_of_str", ["qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",
                                            "qwe",])

foundations.log_param("param_mixed_type", "asdf")
for i in range(20):
  foundations.log_param("param_repeat", f"str{i}")
  sleep(.1)
