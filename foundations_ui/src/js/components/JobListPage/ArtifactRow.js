import React from 'react';
import PropTypes from 'prop-types';

class ArtifactRow extends React.Component {
  constructor(props) {
    super(props);

    this.onClickDownload = this.onClickDownload.bind(this);
  }

  onClickDownload() {
    const { artifact } = this.props;
    window.open(artifact.url);
  }

  render() {
    const { artifact } = this.props;

    return (
      <div className="table-artifacts-row">
        <div className="table-artifacts-row-cell">
          <p>{artifact.name}</p>
        </div>
        <div className="table-artifacts-row-cell last">
          <div className="table-artifacts-row">
            <div
              className="button-download"
              onClick={this.onClickDownload}
              role="button"
              aria-label="Close"
              onKeyDown={this.onKeyDown}
              tabIndex={0}
            >
              <div className="i--icon-download" />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ArtifactRow.propTypes = {
  artifact: PropTypes.object,
};

ArtifactRow.defaultProps = {
  artifact: {},
};

export default ArtifactRow;
