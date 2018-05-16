from vcat import *

def data(path):
  pass

def impute(data_frame, method="mean"):
  pass

def train_it(data_frame, num_layers=2, neurons_per_layer=100, learning_rate=0.01):
  pass

## HOW WE USE/MODIFY HYPERPARAMETERS

# OPTION 1
pipe = pipeline | (data, '/path/to/file') | (impute, "mode") | train_it
pipe.run(num_layers=3, learning_rate=0.1) # CANNOT OVERRIDE path IN data OR method IN impute

# OPTION 2
pipe = pipeline | (data, {"path": pipeline.hyperparameter()} | (impute, pipeline.hyperparameter()) | (train_it, {"num_layers": pipeline.hyperparameter(), "learning_rate": pipeline.hyperparameter()})

curried_pipe = pipe.curry(path='/path/to/file', num_layers=3)
curried_pipe.run(learning_rate=0.2)

# pipeline as an argumentn



# OPTION 3
def hyperparameter(): # IMPLEMENTED ELSEWHERE
  pass

pipe = pipeline | (data, {"path": hyperparameter} | (impute, hyperparameter) | (train_it, {"num_layers": hyperparameter, "learning_rate": hyperparameter})

# BELOW REQUIRES PASSING THE PIPELINE INTO EACH StageConnectorWrapper

pipe.run(path='/path/to/file', num_layers=3, learning_rate=0.1) # CAN OVERRIDE path IN data SINCE IT IS NAMED
pipe.run(path='/path/to/other/file', learning_rate=0.125)

# --------------------------------------------------------------------------------------------------
## HOW WE DO A SEARCH

# OPTION 1
def generator():
  yield {'path': '/path/to/file', 'num_layers': 3, 'learning_rate': 0.1}
  yield {'path': '/path/to/other/file', 'learning_rate': 0.125}

contexts = pipe.hyperparameter_search(generator)

# OPTION 2 (PLUS EVOLUTION)
def run_with_new_params(pipeline, path, num_layers, learning_rate):
  if pipeline.pipeline_context.result["validation_accuracy"] > 0.95:
    # SOME KIND OF DONE LOGIC GOES HERE
    pass
  elif pipeline.pipeline_context.result["validation_accuracy"] > 0.85:
    pipeline.run(num_layers=num_layers + 1, learning_rate=learning_rate * 2).map(run_with_new_params)
  else:
    # SOME KIND OF REJECTION LOGIC GOES HERE
    pass

contexts = pipe.run_async(path='/path/to/file', num_layers=3, learning_rate=0.1).map(run_with_new_params)

# OPTION 3 (WITH GRID SEARCH)
contexts = pipe.hyperparameter_search(num_layers={"min": 2, "max": 10, "number_of_steps": 3}, learning_rate={"min": 0.01, "max": 0.125, "number_of_step": 3}, search_type="grid_search")

# OPTION 4 (GRID SEARCH WITH EVOLUTION)
contexts = pipe.hyperparameter_search_async(num_layers={"min": 2, "max": 10, "number_of_steps": 3}, learning_rate={"min": 0.01, "max": 0.125, "number_of_step": 3}, search_type="grid_search").map(run_with_new_params)

# OPTION 5 (RANDOM SEARCH)
contexts = pipe.hyperparameter_search(num_layers={"min": 2, "max": 10}, learning_rate={"min": 0.01, "max": 0.125}, search_type="random_search", combinations=5)

# OPTION 6 (GUIDED RANDOM SEARCH)
contexts = pipe.hyperparameter_search_aync(num_layers={"min": 2, "max": 10}, learning_rate={"min": 0.01, "max": 0.125}, search_type="random_search", combinations=5).map(run_with_new_params)

## SEARCHING ON A SEARCH???? (HASH'S INTUITIONS)