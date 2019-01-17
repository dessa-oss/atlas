"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ProjectListing(object):

    @staticmethod
    def list_projects(redis_connection):
        """Returns a list of projects store in redis with their 
        creation timestamps

        Arguments:
            redis_connection {RedisConnection} -- Redis connection to use as a provider for data

        Returns:
            list -- The list of project names and creation dates
        """

        from foundations.utils import string_from_bytes

        projects = redis_connection.zrange('projects', 0, -1, withscores=True)
        return [{'name': string_from_bytes(name), 'created_at': created_at} for name, created_at in projects]

    @staticmethod
    def find_project(redis_connection, project_name):
        """Returns a single of projects store in redis with it's 
        creation timestamp

        Arguments:
            redis_connection {RedisConnection} -- Redis connection to use as a provider for data
            project_name {str} -- Name of the project to find

        Returns:
            dict -- The dictionary of the 2 attribute from the description above or None if the project does not exist
        """
        
        created_at = redis_connection.zscore('projects', project_name)
        if created_at is None:
            return None

        return {'name': project_name, 'created_at': created_at}
