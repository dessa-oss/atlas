# Very naive model code
# Each function here can be consider as a step (stage) towards building a model.
import foundations

def incr_by_10(x):
	return x + 10

def mult(x, y):
	foundations.log_metric('x', x)
	foundations.log_metric('y', y)
	output = x * y
	foundations.log_metric('output', output)	
	return output
