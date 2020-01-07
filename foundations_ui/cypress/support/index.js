before(() => {
    cy.exec('python cypress/fixtures/atlas_scheduler/envsubst.py');
});

beforeEach(() => {
  if (Cypress.env('ATLAS_EDITION') === 'TEAM') {
    const schedulerIP = Cypress.env('SCHEDULER_IP');
    cy.exec(`foundations login http://${schedulerIP}:5558 -u test -p test`);
  }
});
