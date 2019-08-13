import React, { Component } from "react";
import PropTypes from "prop-types";
import { Modal, ModalBody } from "reactstrap";

const DefineNewModal = props => {
  const onClickClose = () => {
    props.onClickClose();
  };

  return (
    <div>
      <p>
        Adding a model package can only be done using the command line interface
      </p>
      <button
        type="button"
        onClick={onClickClose}
        className="b--mat b--affirmative"
      >
        OK
      </button>
    </div>
  );
};
DefineNewModal.propTypes = {
  onClickClose: PropTypes.func
};

DefineNewModal.defaultProps = {};
export default DefineNewModal;
