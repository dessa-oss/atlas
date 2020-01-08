import './commands';

before(() => {
  cy.exec('python cypress/fixtures/orbit_acceptance/envsubst.py');
});
