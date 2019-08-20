import React from 'react';

class Readme extends React.Component {
  render() {
    return (
      <div className="readme section-container col-md-4">
        <h2>README.md</h2>
        <textarea placeholder="Type something...">
          Customer churn and engagement has become one
          of the top issues for most banks.
          It costs significantly more to acquire new customers
          than retain existing ones, and it costs far more to
          re-acquire defected customers. In fact, several empirical
          studies and models have proven that churn remains one of
          the biggest destructors of enterprise value for banks and
          other consumer intensive companies.
          1. Introduction
          We aim to accomplish the following for this study:
          Identify and visualize which factors contribute to customer churn:
          Build a prediction model that will perform the following:
          Classify if a customer is going to churn or not
        </textarea>
      </div>
    );
  }
}

export default Readme;
