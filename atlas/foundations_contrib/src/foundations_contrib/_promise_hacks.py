from promise import Promise

def _splat_all(*promises):
    return Promise.all(promises)

def _splat_then(promise, callback):
    def _splat_callback(args):
        return callback(*args)
    return promise.then(_splat_callback)

Promise.splat_all = staticmethod(_splat_all)
Promise.splat_then = _splat_then