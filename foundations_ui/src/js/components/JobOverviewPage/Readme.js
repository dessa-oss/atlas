import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Remarkable } from 'remarkable';

class Readme extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      input: '# This is a header\n\nAnd this is a paragraph',
      editMode: false,
    };

    this.onClickEdit = this.onClickEdit.bind(this);
    this.onChangeMD = this.onChangeMD.bind(this);
    this.renderMD = this.renderMD.bind(this);
  }

  onClickEdit() {
    const { editMode } = this.state;
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
      <div className="readme section-container">
        <h2>README.md</h2>
        <button
          className="button-edit-md"
          type="button"
          onClick={this.onClickEdit}
        >
          {editMode === true ? 'DONE' : 'EDIT'}
        </button>
        {editMode === true && (
          <textarea value={input} onChange={this.onChangeMD} placeholder="Type something..." />
        )}
        {editMode === false && (
          <div dangerouslySetInnerHTML={this.renderMD()} />
        )}
      </div>
    );
  }
}

export default Readme;
