from vcat.stage_connector_wrapper import StageConnectorWrapper

class StageConnectorWrapperFill(object):

    def fill_arg_template(self, new_args, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_args.append(arg.run(**kwargs))
            return True
        return False

    def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_kwargs[keyword] = arg.run(**kwargs)
            return True
        return False
