import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Remarkable } from 'remarkable';
import PropTypes from 'prop-types';
import BaseActions from '../../actions/BaseActions';
import NoDescriptionImage from '../../../assets/svgs/empty-description.svg';

class Readme extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      input: '',
      editMode: false,
      timerId: -1,
    };

    this.onClickEdit = this.onClickEdit.bind(this);
    this.onChangeMD = this.onChangeMD.bind(this);
    this.renderMD = this.renderMD.bind(this);
    this.reload = this.reload.bind(this);
  }

  reload() {
    const { location } = this.props;
    const { projectName } = this.props.match.params;
    let selectedProjectName = location.state && location.state.project ? location.state.project.name : projectName;
    BaseActions.getFromStaging(`projects/${selectedProjectName}/description`).then((result) => {
      result.project_description = String.raw`${result.project_description.replace(/(\r\n|\n|\r)/g, '<br/>')}`;
      let rawDescription = String.raw`${result.project_description}`;
      // eslint-disable-next-line no-useless-escape
      rawDescription = rawDescription.replace(/<br\s*[\/>]?>/gi, '\n');
      rawDescription = rawDescription.replace(/\r/gi, '\n');
      this.setState({
        input: rawDescription,
      });
    });
  }

  componentDidMount() {
    this.reload();
    /* const value = setInterval(() => {
      this.reload();
    }, 10000);
    this.setState({
      timerId: value,
    }); */
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onClickEdit() {
    const { input, editMode } = this.state;
    const { location } = this.props;
    let projectDescription = { project_description: input };
    const { projectName } = this.props.match.params;
    let selectedProjectName = location.state.project ? location.state.project.name : projectName;
    let descriptionUrl = `projects/${selectedProjectName}/description`;

    if (editMode === true) {
      BaseActions.putStaging(descriptionUrl, projectDescription).then((result) => {
        this.reload();
      });
    }

    const value = !editMode;
    this.setState({
      editMode: value,
    });
  }

  onChangeMD(e) {
    this.setState({
      input: e.target.value,
    });
  }

  renderMD() {
    const { input } = this.state;
    const md = new Remarkable();
    return { __html: md.render(input) };
  }

  render() {
    const { input, editMode } = this.state;
    return (
      <div>
        <div className="readme section-container">
          <h3 className="section-title">Project Overview</h3>
          <button
            className={editMode === true ? 'button-edit-md save' : 'button-edit-md'}
            type="button"
            onClick={this.onClickEdit}
          >
            {editMode === true ? 'Save' : 'Edit'}
          </button>
          {editMode === true && (
            <textarea value={input} onChange={this.onChangeMD} placeholder="Type something..." />
          )}
          {editMode === false && input !== '' && (
            <div dangerouslySetInnerHTML={this.renderMD()} />
          )}
          {editMode === false && input === '' && (
            <div className="no-description">
              <h3>Your project overview is empty!</h3>
              <h3>Click on Edit to add a description.</h3>
              <img className="no-description-image" alt="" src={NoDescriptionImage} />
            </div>
          )}
        </div>
      </div>

    );
  }
}

Readme.propTypes = {
  location: PropTypes.object,
  match: PropTypes.object,
};

Readme.defaultProps = {
  location: {},
  match: { params: {} },
};

export default Readme;
