import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';
import ProfilePlaceholder from '../../../assets/images/icons/profile-placeholder.png';
import BaseActions from '../../actions/BaseActions';

class Notes extends React.Component {
  constructor(props) {
    super(props);

    this.onChangeMessage = this.onChangeMessage.bind(this);
    this.onClickAddNote = this.onClickAddNote.bind(this);
    this.reload = this.reload.bind(this);

    this.state = {
      notes: [],
      message: '',
      timerId: -1,
    };
  }

  reload() {
    const { location } = this.props;
    BaseActions.getFromApiary(`projects/${location.state.project.name}/note_listing`).then((result) => {
      if (result) {
        result.sort((a, b) => {
          let dateA = new Date(a.date);
          let dateB = new Date(b.date);
          return dateB - dateA;
        });
        this.setState({
          notes: result,
        });
      }
    });
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 4000);

    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onChangeMessage(e) {
    this.setState({
      message: e.target.value,
    });
  }

  onClickAddNote() {
    const { message } = this.state;
    const { location } = this.props;

    const body = {
      message,
      author: 'Mohammed R.',
    };

    BaseActions.postApiary(`projects/${location.state.project.name}/note_listing`, body).then(() => {
      this.setState({
        message: '',
      }, () => {
        this.reload();
      });
    });
  }

  render() {
    const { notes, message } = this.state;
    return (
      <div className="container-notes">
        <h3 className="section-title">Comments</h3>
        <div className="notes section-container">
          <div className="notes-textarea">
            <textarea placeholder="Add a comment..." value={message} onChange={this.onChangeMessage} />
            <button
              disabled={message === ''}
              className={message === '' ? 'disabled' : ''}
              type="button"
              onClick={this.onClickAddNote}
            >
              Add Note
            </button>
          </div>
          {notes.map((note) => {
            return (
              <div key={note.date} className="notes-blocks">
                <div className="container-note-profile">
                  <img alt="" src={ProfilePlaceholder} />
                  <p>{note.author} <span>{moment(note.date).format('MMMM Do, YYYY').toString()}</span></p>
                </div>
                <p>{note.message}</p>
              </div>
            );
          })}
        </div>
      </div>

    );
  }
}

Notes.propTypes = {
  location: PropTypes.object,
};

Notes.defaultProps = {
  location: { state: {} },
};

export default Notes;
