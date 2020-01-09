describe('Test Invalid Image', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const states = [
    {
      testName: 'Test Invalid Image through the CLI',
      projectName: 'invalid_image_project',
      jobStatus: 'failed',
      logs: '404 Client Error',
      command: 'export FOUNDATIONS_HOME=`pwd`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/invalid_image && foundations submit scheduler invalid_image_project main.py',
    },
    {
      testName: 'Test Invalid Image through the SDK',
      projectName: 'invalid_image_project',
      jobStatus: 'completed',
      logs: '',
      command: 'export FOUNDATIONS_HOME=`pwd`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/invalid_image/invalid_image_project && python main.py',
    },
  ];

  states.forEach(state => {
    describe(state.testName, () => {
      before(() => {
        cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
        cy.exec(state.command);
      });

      beforeEach(() => {
        cy.visit(`http://${guiHost}:${guiPort}/projects`);
      });

      it('Project exists', () => {
        cy.contains(state.projectName).should('exist');
      });

      it('Job status is as expected', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find(`[data-class=job-status-${state.jobStatus}]`)
            .should('exist');
        });
      });

      it('Logs are as expected', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-details-button').click({ force: true });
          cy.get('[data-class=logs-container]').should('contain', state.logs);
        });
      });
    });
  });
});
