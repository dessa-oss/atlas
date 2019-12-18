import React from 'react';
import PropTypes from 'prop-types';
import Layout from '../Layout';
import { withRouter } from 'react-router-dom';
import Schedule from './Schedule';
import Charts from './Charts';
import ModalTutorial from '../../common/ModalTutorial';

const ModelEvaluation = props => {
  const [tutorialVisible, setTutorialVisible] = React.useState(false);

  const onToggleTutorial = () => {
    setTutorialVisible(!tutorialVisible);
  };

  const { tab } = props;

  return (
    <Layout tab={tab} title="Model Evaluation" openTutorial={onToggleTutorial}>
      {/* <Schedule /> */}
      <Charts {...props} />
      <ModalTutorial
        tutorialVisible={tutorialVisible}
        onToggleTutorial={onToggleTutorial}
      />
    </Layout>
  );
};

ModelEvaluation.propTypes = {
  tab: PropTypes.string,
  location: PropTypes.object,
};

ModelEvaluation.defaultProps = {
  tab: 'Evaluation',
  location: { state: {} },
};

export default withRouter(ModelEvaluation);