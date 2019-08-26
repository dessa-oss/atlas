import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Remarkable } from 'remarkable';
import PropTypes from 'prop-types';
import BaseActions from '../../actions/BaseActions';

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
    BaseActions.getFromApiary(`projects/${location.state.project.name}/description`).then((result) => {
      console.log('RELOAD README');
      this.setState({
        input: result.project_description,
      });
    });
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 10000);
    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onClickEdit() {
    const { editMode } = this.state;
    const { location } = this.props;

    if (editMode === true) {
      BaseActions.putApiary(`projects/${location.state.project.name}/description`).then((result) => {
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
        <h3 className="section-title">Project overview</h3>
        <div className="readme section-container">
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
          {editMode === false && (
            <div dangerouslySetInnerHTML={this.renderMD()} />
          )}
        </div>
      </div>

    );
  }
}

Readme.propTypes = {
  location: PropTypes.object,
};

Readme.defaultProps = {
  location: {},
};

export default Readme;
