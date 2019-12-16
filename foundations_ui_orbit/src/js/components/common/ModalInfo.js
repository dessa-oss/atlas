import React from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class ModalInfo extends React.Component {
  constructor(props) {
    super(props);

    this.state = { message: '' };

    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    if (!CommonActions.deepEqual(this.props, prevProps)) {
      this.reload();
    }
  }

  reload() {
    const { fetchInfo } = this.props;

    fetchInfo().then(result => this.setState({ message: result }));
  }

  render() {
    const { message } = this.state;

    return (
      <div className="centered-modal-container">
        {message}
      </div>
    );
  }
}


ModalInfo.propTypes = {
  fetchInfo: PropTypes.func,
};

ModalInfo.defaultProps = {
  fetchInfo: () => {},
};

export default ModalInfo;
