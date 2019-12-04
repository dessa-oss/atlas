import foundations
from time import sleep

foundations.log_metric("str", str(1.))
foundations.log_metric("long str", "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf")
foundations.log_metric("long list of str", ["qwe",
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

foundations.log_metric("mixed_type", "asdf")
for i in range(20):
  foundations.log_metric("repeat", f"str{i}")
  sleep(.1)
