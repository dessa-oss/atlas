import React, { Component } from "react";
import PropTypes from "prop-types";


class OverflowTooltip extends Component {
  constructor(props) {
    super(props);

    this.state = {
      divReference: null
    };
  }

  componentDidMount() {
    if (this.divReference) {
      this.setState({ divReference: this.divReference });
    }
  }

  render() {
    const { divReference } = this.state;
    const { text } = this.props;

    const hasOverflowingChildren = (
      divReference
      && (divReference.offsetHeight < divReference.scrollHeight
      || divReference.offsetWidth < divReference.scrollWidth)
    );

    let tooltip = null;
    if (hasOverflowingChildren) {
      tooltip = (
        <div className="overflow-tooltip-hoverable">
          ...
          <span className="overflow-tooltip">{text}</span>
        </div>
      );
    }

    return (
      <div className="overflow-tooltip-container">
        <div
          className="overflow-tooltip-text"
          ref={divElement => {
            this.divReference = divElement;
          }}
        >{text}
        </div>
        {tooltip}
      </div>
    );
  }
}

OverflowTooltip.propTypes = {
  text: PropTypes.string
};

OverflowTooltip.defaultProps = {
  text: ""
};

export default OverflowTooltip;
