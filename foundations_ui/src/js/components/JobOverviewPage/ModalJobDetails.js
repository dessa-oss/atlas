import React from 'react';
import { Modal, ModalBody } from "reactstrap";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import BaseActions from '../../actions/BaseActions';

class ModalJobDetails extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      tags: [
        "LSTM",
        "probably won't work",
      ],
    };

    this.onClickRemoveTag = this.onClickRemoveTag.bind(this);
  }

  componentDidMount(){
    const { job, location } = this.props;
    BaseActions.getFromApiary('projects/' + location.state.project.name + '/jobs/' + job.id + '/tags').then(result => {
      this.setState({
        tage: result,
      });
    });
  }

  onClickRemoveTag(tag) {
    console.log(tag);
  }

  render() {
    const { job, visible, onToggle } = this.props;
    const { tags } = this.state;

    return (
      <Modal
        isOpen={visible}
        toggle={onToggle}
        className="modal-job-details"
      >
        <ModalBody>
          <div className="contanier-main">
            <div className="container-title">
              <p className="label-id">Details For Job</p>
              <div className="container-id">
                <p className="text-id">{job.id}</p>
                <div className="icon-copy" />
              </div>
              <div className="icon-close" onClick={onToggle} />
            </div>
            <div className="container-tags">
              {tags.map(tag => {
                return (
                  <div className="container-tag">
                    <p className="text-tag">{tag}</p>
                    <div className="icon-remove" onClick={this.onClickRemoveTag} />
                  </div>
                );
              })}
              <div className="icon-add">+</div>
            </div>
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


ModalJobDetails.propTypes = {
  visible: PropTypes.bool,
  onToggle: PropTypes.func
};

ModalJobDetails.defaultProps = {
  visible: false,
  onToggle: () => null
};

export default withRouter(ModalJobDetails);