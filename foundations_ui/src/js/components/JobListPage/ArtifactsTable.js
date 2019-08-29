import React from 'react';
import PropTypes from 'prop-types';
import ArtifactRow from './ArtifactRow';

class ArtifactsTable extends React.Component {
  render() {
    const { job } = this.props;
    return (
      <div className="container-artifacts-table">
        <div className="table-artifacts-header">
          <p>Artifact Name</p>
        </div>
        <div className="table-artifacts-header last" />
        {job.artifacts.map((artifact) => {
          return <ArtifactRow key={artifact.id} artifact={artifact} />;
        })}
      </div>
    );
  }
}

ArtifactsTable.propTypes = {
  job: PropTypes.object,
  location: PropTypes.object,
};

ArtifactsTable.defaultProps = {
  job: {},
  location: { state: {} },
};

export default ArtifactsTable;
