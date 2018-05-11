# writing results

# have a dataset, done training
pipeline_context = PipelineContext("name_of_pipeline")
pipeline_context = PipelineContext("description_of_pipeline")

# min user info that describes pipeline context
# will help understand results later if done correctly
# hyperparameters will be automatically tracked and added to pipeline


for epoch in range(epoch_count):
  model.train(num_of_interations)
  loss = model.get_loss()
  pipeline_context.results.loss[epoch] = loss # option 1
  pipeline_context.results.loss.append(loss) # option 2
  pipeline_context.results.add_loss(loss) # option 3
  pipeline_context.results.louu[epoch] = loss # option 1

roc_auc = model.get_roc_auc()
pipeline_context.results.roc_auc = roc_auc # option 1
pipeline_context.results.set_roc_auc(roc_auc) # option 2

mdr5 = model.get_mdr(threshold=0.5)
pipeline_context.results.mdr5 = mdr5

pipeline_context.save()
