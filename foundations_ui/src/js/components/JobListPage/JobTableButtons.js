import React, { Component } from 'react';

class JobTableButtons extends Component {
  render() {
    return (
      <div className="job-details-header">
        <button type="button"><span className="i--icon-tf" /> <p className="text-upper">Send to tensorboard</p></button>
        <button type="button" className="text-upper">Delete</button>
        <select>
          <option> Filter Columns </option>
        </select>
      </div>
    );
  }
}

export default JobTableButtons;
