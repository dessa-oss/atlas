JIRA Ticket link:

For Reviewer:

* Do acceptance tests properly cover AC?
* Do acceptance tests match real user behaviour?
* Think about how you would have solved the problem:
   * Look for abstractions.
   * Think like an adversary, but be nice about it.
   * Think about libraries or existing product code.
   * Does the change add compile-time or run-time dependencies (especially between sub-projects)?
* Does the PR only cover 1 subtask, and no more than that
* Critique data and distribution of features for acceptance tests

Checklist for pull request:

- [] All unit tests pass
- [] All examples pass
- [] All integration tests pass
- [] All acceptance tests pass
- [] Acceptance tests that fulfill AC for ticket should be created and pass
- [] Have tested both remote and local deployment types
- [] All necessary documentation and READMEs have been updated
- [] Pick realistic type of data (not large, but a good distribution of features) for acceptance tests