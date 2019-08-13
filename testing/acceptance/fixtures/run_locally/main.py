import foundations
from foundations_contrib.global_state import current_foundations_context

foundations.log_metric('ugh', 10)

with open('thomas_text.txt', 'w') as f:
    f.write('ugh_square')

foundations.save_artifact('thomas_text.txt', 'just_some_artifact')
foundations.log_param('blah', 20)

print(current_foundations_context().pipeline_context().job_id)