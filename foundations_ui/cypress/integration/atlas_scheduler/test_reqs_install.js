describe('Test Requirements Install', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const command = 'export FOUNDATIONS_HOME=`pwd`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/reqs_install && foundations login http://localhost:5558 -u test -p test && foundations submit scheduler reqs_install_project main.py testarg1 testarg2';
  const projectName = 'reqs_install_project';
  const expectedLogs = 'xgboost';

  before(() => {
    cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
    cy.exec(command);
  });

  beforeEach(() => {
    cy.visit(`http://${guiHost}:${guiPort}/projects`);
  });

  it('Project exists', () => {
    cy.contains(projectName).should('exist');
  });

  it('Job status is as expected', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-table-row]')
        .find('[data-class=job-status-completed]')
        .should('exist');
    });
  });

  it('Logs are as expected', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-details-button').click({ force: true });
      cy.get('[data-class=logs-container]').should('contain', expectedLogs);
    });
  });
});
