import React from "react";
import { Modal, ModalBody } from "reactstrap";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";

class ModalTutorial extends React.Component {
  constructor(props) {
    super(props);

    this.onClickNext = this.onClickNext.bind(this);
    this.onClickPrevious = this.onClickPrevious.bind(this);

    this.state = {
      imageIndex: 1
    };
  }

  onClickNext() {
    const { imageIndex } = this.state;

    if (imageIndex < 5) {
      this.setState(prevState => {
        let value = prevState.imageIndex + 1;
        return {
          ...prevState,
          imageIndex: value
        };
      });
    }
  }

  onClickPrevious() {
    const { imageIndex } = this.state;

    if (imageIndex > 1) {
      this.setState(prevState => {
        let value = prevState.imageIndex - 1;
        return {
          ...prevState,
          imageIndex: value
        };
      });
    }
  }

  render() {
    const { tutorialVisible, onToggleTutorial } = this.props;
    const { imageIndex } = this.state;

    let containerClassName = "container-tutorial image-1";

    if (imageIndex === 2) {
      containerClassName = "container-tutorial image-2";
    }

    if (imageIndex === 3) {
      containerClassName = "container-tutorial image-3";
    }

    if (imageIndex === 4) {
      containerClassName = "container-tutorial image-4";
    }

    if (imageIndex === 5) {
      containerClassName = "container-tutorial image-5";
    }

    return (
      <Modal
        isOpen={tutorialVisible}
        toggle={onToggleTutorial}
        className="modal-tutorial"
      >
        <ModalBody>
          <div className={containerClassName}>
            <div className="container-tutorial-dots">
              <div
                className={
                  imageIndex === 1
                    ? "tutorial-dot-active"
                    : "tutorial-dot-inactive"}
              />
              <div
                className={
                  imageIndex === 2
                    ? "tutorial-dot-active"
                    : "tutorial-dot-inactive"}
              />
              <div
                className={
                  imageIndex === 3
                    ? "tutorial-dot-active"
                    : "tutorial-dot-inactive"}
              />
              <div
                className={
                  imageIndex === 4
                    ? "tutorial-dot-active"
                    : "tutorial-dot-inactive"}
              />
              <div
                className={
                  imageIndex === 5
                    ? "tutorial-dot-active"
                    : "tutorial-dot-inactive"}
              />
            </div>
            {
              imageIndex !== 5 && (
                <div
                  className="button-tutorial-next"
                  onClick={this.onClickNext}
                >
                  NEXT
                </div>
              )
            }
            {
              imageIndex !== 1 && (
                <div
                  className="button-tutorial-previous"
                  onClick={this.onClickPrevious}
                >
                  BACK
                </div>
              )
            }
            {/* <div
              className="button-tutorial-close"
              onClick={onToggleTutorial}
            >
              X
            </div> */}
          </div>
        </ModalBody>
      </Modal>
    );
  }
}

ModalTutorial.propTypes = {
  tutorialVisible: PropTypes.bool,
  onToggleTutorial: PropTypes.func
};

ModalTutorial.defaultProps = {
  tutorialVisible: false,
  onToggleTutorial: () => null
};

export default withRouter(ModalTutorial);
