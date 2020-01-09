describe('Test Fast Job', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const projectName = 'fast_job_project';

  const states = [
    {
      testName: 'Test Ten Fast Jobs through CLI',
      projectName: projectName,
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/fast_job/ && foundations submit scheduler ${projectName} main.py &`,
    },
    {
      testName: 'Test Ten Fast Jobs through SDK',
      projectName: projectName,
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/fast_job/${projectName}/ && python main.py &`,
    },
  ];

  states.forEach(state => {
    describe(state.testName, () => {
      before(() => {
        cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);

        for (let i = 0; i < 9; i += 1) {
          cy.exec(state.command);
        }
        cy.exec(state.command.substring(0, state.command.length - 1));
      });

      beforeEach(() => {
        cy.visit(`http://${guiHost}:${guiPort}/projects`);
      });

      it('Project exists', () => {
        cy.contains(state.projectName).should('exist');
      });

      it('Job exists on projects page', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]').should('exist');
        });
      });

      it('Job is completed', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find('[data-class=job-status-completed]')
            .should('exist');
        });
      });
    });
  });
});
