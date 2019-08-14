import foundations

def eval(eval_period):
    foundations.track_production_metrics('roc_auc', {eval_period: 66})
    foundations.track_production_metrics('MSE', {eval_period: 1, f'{eval_period}_again': 2})