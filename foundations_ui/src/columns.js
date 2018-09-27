const completed_columns = [{
    Header: 'Start Time',
    accessor: 'start_time'
  }, {
    Header: 'Status',
    accessor: 'status'
  }, {
    Header: 'JobId',
    accessor: 'job_id'
  }, {
    Header: 'User',
    accessor: 'user'
  }
]

module.exports.completed_columns = completed_columns

const queued_columns = [{
    Header: 'Start Time',
    accessor: 'submitted_time'
  }, {
    Header: 'JobId',
    accessor: 'job_id'
  }, {
    Header: 'Duration in Queue',
    accessor: 'start_time'
  }, {
    Header: 'User',
    accessor: 'user'
  }
]

module.exports.queued_columns = queued_columns