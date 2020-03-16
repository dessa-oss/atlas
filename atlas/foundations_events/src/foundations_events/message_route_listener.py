
class MessageRouteListener(object):
    """
    Template Listener to subscribe to a MessageRoute
    """
    
    def call(self, message):
        """
        Method returns message it was called with

        Arguments:
            message {json seriablizable data} -- message for the listener to return
        """
        return message