import React, { Component } from 'react';
import PropTypes from 'prop-types';
import OverflowTooltip from '../../common/OverflowTooltip';

class MonitorListTableRow extends Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
  }

  onClick() {
    const { onClick, monitorName } = this.props;

    onClick(monitorName);
  }

  isSelectedRow() {
    const { selectedRow, monitorName } = this.props;
    return monitorName === selectedRow;
  }

  render() {
    const {
      monitorNameLabel,
      status,
      user,
    } = this.props;

    const selectedClass = this.isSelectedRow() ? 'selected-row' : '';

    function addStatus(rowStatus) {
      if (rowStatus === 'paused') {
        return <div className="status-icon status-paused-orange" />;
      }

      if (rowStatus === 'active') {
        return <div className="status-icon status-green" />;
      }
    }

    const statusIcon = addStatus(status);

    return (
      <div className={`monitor-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="monitor-table-cell" data-class="monitor-name"><OverflowTooltip text={monitorNameLabel} /></div>
        <div className="monitor-user-table-cell"><OverflowTooltip text={user} /></div>
        <div className="monitor-status-table-cell">{statusIcon}</div>
      </div>
    );
  }
}

MonitorListTableRow.propTypes = {
  monitorName: PropTypes.string,
  monitorNameLabel: PropTypes.string,
  status: PropTypes.string,
  user: PropTypes.string,
  onClick: PropTypes.func,
  selectedRow: PropTypes.string,
};

MonitorListTableRow.defaultProps = {
  monitorName: 'Invalid monitor name',
  monitorNameLabel: 'Invalid monitor name',
  status: 'Invalid contract name',
  user: '',
  onClick: () => {},
  selectedRow: '',
};


export default MonitorListTableRow;
