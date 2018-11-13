"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

class MessageRouter(object):
    """
    This singleton class and manages the MessageRoutes by creating MessageRoute objects and assigning them MessageRouteListeners
    """

    class __MessageRouter:
        def __init__(self):
            self.routes = []

        def add_listener(self, listener, route_name):
            """
            Adds listener to route. Creates route if none exists. 

            Arguments:
                listener {MessageRouteListener} -- listener to add to route
                route_name {string} -- name of route to add listener to
            """
            from foundations.message_route import MessageRoute

            foundName = False

            for route in self.routes:
                if route_name == route.get_name():
                    route.add_listener(listener)
                    foundName = True

            if foundName == False:
                new_route = MessageRoute(route_name)
                new_route.add_listener(listener)
                self.routes.append(new_route)
            
        def push_message(self, route_name, message, metadata = None):
            """
            Pushes message and metadata (None by default) to a route

            Arguments:
                route_name {string} -- name of route to send message to
                message {dictionary} -- message to send to route
                metadata {dictionary} -- default to None
            """
            for route in self.routes:
                if route_name == route.get_name():
                    route.push_message(message, metadata)
        
        def _in_route(self, route_name):
            for route in self.routes:
                if route_name == route.get_name():
                    return True
            return False
        
        def reset_routes(self):
            """
            Empties the list of MessageRoute objects
            """
            self.routes = []
        

    instance = None
    def __init__(self):
        if not MessageRouter.instance:
            MessageRouter.instance = MessageRouter.__MessageRouter()

    def __getattr__(self, name):
        return getattr(self.instance, name)
