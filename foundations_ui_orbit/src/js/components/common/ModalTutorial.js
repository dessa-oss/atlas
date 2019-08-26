import React from "react";
import { Modal, ModalBody } from "reactstrap";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import ImageTutorial1 from "../../../assets/images/tutorial_1.png";
import ImageTutorial2 from "../../../assets/images/tutorial_2.png";
import ImageTutorial3 from "../../../assets/images/tutorial_3.png";
import ImageTutorial4 from "../../../assets/images/tutorial_4.png";
import ImageTutorial5 from "../../../assets/images/tutorial_5.png";


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

  renderImageTutorial() {
    const { imageIndex } = this.state;

    if (imageIndex === 2) {
      return <img alt="" src={ImageTutorial2} />;
    }

    if (imageIndex === 3) {
      return <img alt="" src={ImageTutorial3} />;
    }

    if (imageIndex === 4) {
      return <img alt="" src={ImageTutorial4} />;
    }

    if (imageIndex === 5) {
      return <img alt="" src={ImageTutorial5} />;
    }

    return <img alt="" src={ImageTutorial1} />;
  }

  render() {
    const { tutorialVisible, onToggleTutorial } = this.props;
    const { imageIndex } = this.state;

    return (
      <Modal
        isOpen={tutorialVisible}
        toggle={onToggleTutorial}
        className="modal-tutorial"
      >
        <ModalBody>
          <div className="container-tutorial">
            {this.renderImageTutorial()}
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
