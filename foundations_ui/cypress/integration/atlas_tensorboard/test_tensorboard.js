describe('Test Tensorboard', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const atlasRestAPIPort = Cypress.env('ATLAS_REST_API_PORT');

  const states = [
    {
      testName: 'Test Submit Tensorboard Job',
      projectName: 'tensorboard_job',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && cd cypress/fixtures/tensorboard_job && python -m foundations submit scheduler . tensorboard_job.py`,
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

      it('Job is completed, and has tensorboard tag', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find('[data-class=job-status-completed]')
            .should('exist');
          cy.get('[data-class=job-table-row]')
            .find('[data-class=i--icon-tf]')
            .should('exist');
        });
      });
    });
  });
});
