import foundations

def add(x,y):
    result = x + y
    foundations.log_metric('Score', result)
    return result

def subtract(x,y):
    result = x - y
    return result
