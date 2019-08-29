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

    console.log('JOB: ', job);

    this.state = {
      tags: [],
      tab: 'logs',
      newTag: '',
      timerId: -1,
      addNewTagVisible: false,
      job,
    };

    this.onClickRemoveTag = this.onClickRemoveTag.bind(this);
    this.onClickLogs = this.onClickLogs.bind(this);
    this.onClickArtifacts = this.onClickArtifacts.bind(this);
    this.onChangeTagName = this.onChangeTagName.bind(this);
    this.onClickShowAddTag = this.onClickShowAddTag.bind(this);
    this.onClickAddNewTag = this.onClickAddNewTag.bind(this);
    this.onClickCancelAddNewTag = this.onClickCancelAddNewTag.bind(this);
  }

  reload() {
    const { location } = this.props;
    const { job } = this.state;
    BaseActions.getFromStaging(`projects/${location.state.project.name}/job_listing`)
      .then((result) => {
        const filteredJob = result.jobs.find(item => item.job_id === job.job_id);
        let newTags = [];
        if (filteredJob.tags) {
          if (Array.isArray(filteredJob.tags)) {
            newTags = filteredJob.tags;
          } else {
            newTags = Object.keys(filteredJob.tags);
          }
        }
        this.setState({
          addNewTagVisible: false,
          tags: newTags,
          job: filteredJob,
        });
      });
  }

  componentDidMount() {
    this.reload();
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  onToggleModal() {
    const { onToggle } = this.props;
    const { job } = this.state;
    onToggle(job);
  }

  onClickShowAddTag() {
    this.setState({
      addNewTagVisible: true,
    });
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

  onKeyDown() { }

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

  onChangeTagName(e) {
    this.setState({
      newTag: e.target.value,
    });
  }

  onClickAddNewTag() {
    const { newTag, job } = this.state;
    const { location } = this.props;
    BaseActions.postApiary(`projects/${location.state.project.name}/job_listing/${job.job_id}/tags`)
      .then((result) => {
        this.reload();
      });
  }

  onClickCancelAddNewTag() {
    this.setState({
      addNewTagVisible: false,
    });
  }

  render() {
    const { visible, onToggle } = this.props;
    const {
      tags,
      tab,
      addNewTagVisible,
      job,
    } = this.state;

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
                onClick={this.onClickShowAddTag}
                role="button"
                aria-label="Add Tag"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              >
                +
              </div>
              {addNewTagVisible === true
                && (
                  <div className="container-add-new-tag">
                    <input onChange={this.onChangeTagName} placeholder="Insert tag" />
                    <button type="button" onClick={this.onClickAddNewTag}>SAVE</button>
                    <button type="button" onClick={this.onClickCancelAddNewTag}>CANCEL</button>
                  </div>
                )}
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
