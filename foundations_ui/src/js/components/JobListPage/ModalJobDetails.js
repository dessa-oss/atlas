import React from 'react';
import { Modal, ModalBody } from 'reactstrap';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { toast } from 'react-toastify';
import BaseActions from '../../actions/BaseActions';
import Tag from '../common/Tag';
import ArtifactsTable from './ArtifactsTable';
import Logs from './Logs';

class ModalJobDetails extends React.Component {
  constructor(props) {
    super(props);

    const { job } = this.props;

    this.state = {
      tags: [
        'LSTM',
        'probably won\'t work',
      ],
      tab: 'logs',
      timerId: -1,
    };

    this.onClickRemoveTag = this.onClickRemoveTag.bind(this);
    this.onClickLogs = this.onClickLogs.bind(this);
    this.onClickArtifacts = this.onClickArtifacts.bind(this);
  }

  reload() {
    const { job, location } = this.props;

    if (Array.isArray(job.tags)) {
      this.setState({
        tags: job.tags,
      });
    } else {
      const tags = Object.keys(job.tags);
      this.setState({
        tags,
      });
    }

    // this.setState({
    //   tags: job.tags,
    // });
    // BaseActions.getFromApiary(`projects/${location.state.project.name}/jobs/${job.id}/tags`).then((result) => {
    //   if (result) {
    //     this.setState({
    //       tags: job.tags,
    //     });
    //   }
    // });
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 4000);
    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onToggleModal() {
    const { onToggle, job } = this.props;
    onToggle(job);
  }

  onClickAddTag() {
    console.log('add tag');
  }

  onClickRemoveTag() {
    console.log('remove tag');
  }

  notifiedCopy(e) {
    e.stopPropagation();
    toast.info('Job ID successfully copied', {
      autoClose: 1500,
      draggable: false,
    });
  }

  onKeyDown() {}

  onClickLogs() {
    this.setState({
      tab: 'logs',
    });
  }

  onClickArtifacts() {
    this.setState({
      tab: 'artifacts',
    });
  }

  render() {
    const { job, visible, onToggle } = this.props;
    const { tags, tab } = this.state;

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
                <p className="text-id">{job.job_id}</p>
                <CopyToClipboard text={job.job_id}>
                  <span
                    onClick={this.notifiedCopy}
                    className="i--icon-copy"
                    role="presentation"
                  />
                </CopyToClipboard>
              </div>
              <div
                className="close"
                onClick={onToggle}
                role="button"
                aria-label="Close"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              />
            </div>
            <div className="container-tags">
              {tags.map((tag) => {
                return <Tag key={tag} value={tag} />;
              })}
              <div
                className="button-add"
                onClick={this.onClickAddTag}
                role="button"
                aria-label="Add Tag"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              >
                +
              </div>
            </div>
            <div className="container-tabs">
              <div>
                <h3
                  className={tab === 'logs' ? 'active' : ''}
                  onClick={this.onClickLogs}
                  onKeyDown={this.onKeyDown}
                >
                  Logs
                </h3>
                <h3
                  className={tab === 'artifacts' ? 'active' : ''}
                  onClick={this.onClickArtifacts}
                  onKeyDown={this.onKeyDown}
                >
                  Artifacts
                </h3>
              </div>
            </div>
            {tab === 'logs' && <Logs job={job} {...this.props} />}
            {tab === 'artifacts' && (
              <div className="container-artifacts">
                <div className="image-artifacts" />
                <ArtifactsTable />
              </div>
            )}
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


ModalJobDetails.propTypes = {
  job: PropTypes.object,
  visible: PropTypes.bool,
  onToggle: PropTypes.func,
  location: PropTypes.object,
};

ModalJobDetails.defaultProps = {
  job: {},
  visible: false,
  onToggle: () => null,
  location: { state: {} },
};

export default withRouter(ModalJobDetails);
