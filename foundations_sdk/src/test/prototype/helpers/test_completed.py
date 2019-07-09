"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers import *
from foundations_spec.extensions import *
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn

import random

class TestCompletedJobHelpers(Spec):
    
    redis = let_fake_redis()

    @let
    def listing(self):
        return {self._random_uuid() for _ in range(self.job_count)}

    @let
    def job_count(self):
        import random
        return random.randint(2, 10)

    @let
    def random_job_id(self):
        return random.choice(list(self.listing))

    @let
    def random_job_id_two(self):
        return random.choice(list(self.listing - {self.random_job_id}))

    @let
    def project_name(self):
        return self.faker.name()

    @let
    def project_name_two(self):
        return self.faker.name()

    @set_up
    def set_up(self):
        for job_id in self.listing:
            self.redis.sadd('projects:global:jobs:completed', job_id)

    def test_list_jobs_returns_all_completed_jobs(self):
        from foundations.prototype.helpers.completed import list_jobs
        self.assertEqual(self.listing, list_jobs(self.redis))

    def test_job_project_names_returns_project_names(self):
        from foundations_contrib.consumers.jobs.queued.project_name import ProjectName
        from foundations.prototype.helpers.completed import job_project_names

        consumer = ProjectName(self.redis)
        consumer.call({'project_name': self.project_name, 'job_id': self.random_job_id}, None, {})
        consumer.call({'project_name': self.project_name_two, 'job_id': self.random_job_id_two}, None, {})
        
        result = job_project_names(self.redis, [self.random_job_id, self.random_job_id_two])
        expected = {self.random_job_id: self.project_name, self.random_job_id_two: self.project_name_two}
        self.assertEqual(expected, result)

    def test_list_archived_jobs_returns_all_archived_jobs(self):
        from foundations.prototype.helpers.completed import list_archived_jobs

        for job_id in self.listing:
            self.redis.sadd('projects:global:jobs:archived', job_id)
        self.assertEqual(self.listing, list_archived_jobs(self.redis))

    def test_remove_jobs_removes_all_completed_jobs(self):
        from foundations.prototype.helpers.completed import remove_jobs, list_jobs
        remove_jobs(self.redis, {self.random_job_id: self.project_name})
        self.assertEqual(self.listing - {self.random_job_id}, list_jobs(self.redis))

    def test_remove_jobs_removes_all_completed_jobs_from_projects(self):
        from foundations_contrib.consumers.jobs.queued.project_listing import ProjectListing
        from foundations.prototype.helpers.completed import remove_jobs, list_jobs

        ProjectListing(self.redis).call({'project_name': self.project_name, 'job_id': self.random_job_id}, None, {})
        ProjectListing(self.redis).call({'project_name': self.project_name, 'job_id': self.random_job_id_two}, None, {})
        remove_jobs(self.redis, {self.random_job_id: self.project_name})
        project_job_count = self.redis.scard('project:{}:jobs:running'.format(self.project_name))
        self.assertEqual(1, project_job_count)

    def test_remove_jobs_removes_all_completed_jobs_multiple_jobs(self):
        from foundations.prototype.helpers.completed import remove_jobs, list_jobs
        remove_jobs(self.redis, {self.random_job_id: self.project_name, self.random_job_id_two: self.project_name_two})
        self.assertEqual(self.listing - {self.random_job_id, self.random_job_id_two}, list_jobs(self.redis))

    def test_add_jobs_to_archive_adds_job_to_archive(self):
        from foundations.prototype.helpers.completed import add_jobs_to_archive
        add_jobs_to_archive(self.redis, [self.random_job_id])
        self.assertEqual({self.random_job_id.encode('utf-8')}, self.redis.smembers('projects:global:jobs:archived'))

    def test_add_jobs_to_archive_adds_jobs_to_archive_multiple_jobs(self):
        from foundations.prototype.helpers.completed import add_jobs_to_archive
        add_jobs_to_archive(self.redis, [self.random_job_id, self.random_job_id_two])
        self.assertEqual({self.random_job_id.encode('utf-8'), self.random_job_id_two.encode('utf-8')}, self.redis.smembers('projects:global:jobs:archived'))

    def _random_uuid(self):
        from uuid import uuid4
        return str(uuid4())