import foundations

def log_predictions_for_assertion(predictions):
    for prediction in predictions["Survived"]:
        foundations.log_metric("predictions", prediction)

