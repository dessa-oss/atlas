import React from 'react';
import PropTypes from 'prop-types';

class ArtifactRow extends React.Component {
  constructor(props) {
    super(props);

    this.onClickDownload = this.onClickDownload.bind(this);
    this.onClickThisArtifact = this.onClickThisArtifact.bind(this);
  }

  onClickDownload() {
    const { artifact } = this.props;
    window.open(artifact.uri);
  }

  onClickThisArtifact() {
    const { onClickArtifact, artifact } = this.props;
    onClickArtifact(artifact);
  }

  render() {
    const { artifact } = this.props;

    return (
      <div
        tabIndex="0"
        onKeyPress={this.onClickThisArtifact}
        role="button"
        onClick={this.onClickThisArtifact}
        className="table-artifacts-row"
      >
        <div className="table-artifacts-row-cell">
          <p>{artifact.filename}</p>
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
  onClickArtifact: PropTypes.func,
};

ArtifactRow.defaultProps = {
  artifact: {},
  onClickArtifact: () => {},
};

export default ArtifactRow;
