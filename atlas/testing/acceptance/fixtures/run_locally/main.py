import foundations
from foundations_contrib.global_state import current_foundations_job, redis_connection

foundations.log_metric('ugh', 10)

with open('thomas_text.txt', 'w') as f:
    f.write('ugh_square')

foundations.save_artifact('thomas_text.txt', 'just_some_artifact')
foundations.log_param('blah', 20)

redis_connection.set('foundations_testing_job_id', current_foundations_job().job_id)
