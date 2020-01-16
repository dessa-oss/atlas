before(() => {
  cy.exec('python cypress/fixtures/atlas_scheduler/envsubst.py');
});

beforeEach(() => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  cy.visit(`http://${guiHost}:${guiPort}`);
  cy.get('input[name=username]').type('test', { force: true });
  cy.get('input[name=password]').type('test', { force: true });
  cy.get('.login-submit').click({ force: true });
  cy.wait(200);

  cy.exec(`foundations login http://${schedulerIP}:5558 -u test -p test`);
});
