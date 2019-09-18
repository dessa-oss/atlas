import React from 'react';
import PropTypes from 'prop-types';
import BaseActions from '../../actions/BaseActions';

class Header extends React.Component {
  constructor(props) {
    super(props);
    let name = '';
    let createdAt = '';
    let owners = '';

    if (this.props.location.state && this.props.location.state.project && this.props.location.state.project !== {}) {
      name = this.props.location.state.project.name;
      createdAt = this.props.location.state.project.created_at;
      owners = this.props.location.state.project.owner;
    }

    this.state = {
      name,
      dateCreated: createdAt,
      projectOwners: owners,
    };

    this.onClickBack = this.onClickBack.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  async reload() {
    const { name, dateCreated, projectOwners } = this.state;

    if (name === '' || dateCreated === '' || projectOwners === '') {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.getFromStaging('projects');
      const selectedProject = fetchedProjects.filter(item => item.name === projectName)[0];
      if (selectedProject && selectedProject.length > 0) {
        this.setState({
          name: selectedProject.name,
          dateCreated: selectedProject.created_at,
          projectOwners: selectedProject.owner,
        });
      }
    }
  }

  componentDidMount() {
    this.reload();
  }

  onClickBack() {
    const { history } = this.props;
    history.push(
      '/projects',
    );
  }

  onKeyDown() {}

  render() {
    const { name, dateCreated, projectOwners } = this.state;

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
            <h1 className="font-bold">{name}</h1>
          </div>
          <div>
            <div className="container-label-date font-bold">Date Created: </div>
            <div className="container-text-date">{dateCreated}</div>
          </div>
          <div>
            <div className="container-label-date font-bold">Project Owners: </div>
            <div className="container-text-date">CE User</div>
          </div>
        </div>
      </div>
    );
  }
}

Header.propTypes = {
  history: PropTypes.object,
  location: PropTypes.object,
  match: PropTypes.object,

};

Header.defaultProps = {
  history: {},
  location: {},
  match: { params: {} },
};

export default Header;
