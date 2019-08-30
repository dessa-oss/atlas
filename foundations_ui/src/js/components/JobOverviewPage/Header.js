import React from 'react';
import PropTypes from 'prop-types';

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.history.location.state.project.name,
      dateCreated: this.props.history.location.state.project.created_at,
      projectOwners: this.props.history.location.state.project.owner,
    };

    this.onClickBack = this.onClickBack.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  onClickBack() {
    const { history } = this.props;
    history.goBack();
  }

  onKeyDown() {}

  render() {
    const { projectName, dateCreated, projectOwners } = this.state;

    return (
      <div>
        <div className="job-overview-header-container">
          <div>
            <h3
              className="text-project-directory"
              onClick={this.onClickBack}
              aria-label="Go Back"
              onKeyDown={this.onKeyDown}
            >
              <i
                className="icono-arrow1-right"
              />
              Project Directory
            </h3>
            <h1 className="font-bold">{projectName}</h1>
          </div>
          <div>
            <div className="container-label-date font-bold">Date Created: </div>
            <div className="container-text-date">{dateCreated}</div>
          </div>
          <div>
            <div className="container-label-date font-bold">Project Owners: </div>
            <div className="container-text-date">{projectOwners}</div>
          </div>
        </div>
      </div>
    );
  }
}

Header.propTypes = {
  history: PropTypes.object,

};

Header.defaultProps = {
  history: {},
};

export default Header;
