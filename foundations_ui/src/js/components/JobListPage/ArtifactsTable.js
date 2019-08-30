import React from 'react';
import PropTypes from 'prop-types';
import ArtifactRow from './ArtifactRow';

class ArtifactsTable extends React.Component {
  render() {
    const { job, onClickArtifact } = this.props;
    return (
      <div className="container-artifacts-table">
        <div className="table-artifacts-header">
          <p>Artifact Name</p>
        </div>
        <div className="table-artifacts-header last" />
        {job.artifacts ? job.artifacts.map((artifact) => {
          return <ArtifactRow onClickArtifact={onClickArtifact} key={artifact.id} artifact={artifact} />;
        }) : null
        }
      </div>
    );
  }
}

ArtifactsTable.propTypes = {
  job: PropTypes.object,
  location: PropTypes.object,
  onClickArtifact: PropTypes.func,
};

ArtifactsTable.defaultProps = {
  job: {},
  location: { state: {} },
  onClickArtifact: () => {},
};

export default ArtifactsTable;
