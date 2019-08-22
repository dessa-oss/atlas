import React from 'react';
import moment from 'moment';
import ProfilePlaceholder from '../../../assets/images/icons/profile-placeholder.png';

class Notes extends React.Component {
  constructor(props) {
    super(props);

    this.onChangeMessage = this.onChangeMessage.bind(this);
    this.onClickAddNote = this.onClickAddNote.bind(this);

    this.state = {
      notes: [{
        id: 1,
        date: '2019-06-25',
        author: 'Mohammed R.',
        message: 'This is my message to you',
      }],
      message: '',
    };
  }

  onChangeMessage(e) {
    this.setState({
      message: e.target.value,
    });
  }

  onClickAddNote() {
    const { message, notes } = this.state;

    const newNote = {
      id: notes[notes.length - 1].id + 1,
      date: moment().toString(),
      author: 'Mohammed R.',
      message,
    };

    const newNotes = notes;
    newNotes.push(newNote);

    newNotes.sort((a, b) => {
      let dateA = new Date(a.date);
      let dateB = new Date(b.date);

      return dateB - dateA;
    });

    this.setState({
      notes: newNotes,
      message: '',
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
            <button type="button" onClick={this.onClickAddNote}>Add Note</button>
          </div>
          {notes.map((note) => {
            return (
              <div key={note.id} className="notes-blocks">
                <div className="container-note-profile">
                  <img alt="" src={ProfilePlaceholder} />
                  <div className="container-name-date">
                    <p>{note.author} <span>{moment(note.date).format('MMMM Do, YYYY').toString()}</span></p>
                  </div>
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

export default Notes;
