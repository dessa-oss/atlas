import foundations

def add(x,y):
    result = x + y
    foundations.log_metric('Score', result)
    return result