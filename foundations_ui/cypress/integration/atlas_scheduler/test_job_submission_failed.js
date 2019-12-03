describe('Test Job Submission that Fails', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const states = [
    {
        testName: `Test Job Submission that Fails with CLI with project job_submission_project`,
        projectName: 'job_submission_project',
        command: 'export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations submit scheduler job_submission_project main.py 0 "Complete_Failed_Task_1"'
      },
      {
        testName: `Test Job Submission that Fails with CLI with project job_submission_project_with_foundations`,
        projectName: 'job_submission_project_with_foundations',
        command: 'export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations submit scheduler job_submission_project_with_foundations main.py 0 "Complete_Failed_Task_2"'
      }
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

      it('Job exists on projects page', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
         cy.get('[data-class=job-table-row]').should('exist');
        });
      });

      it('Job has failed', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
         cy.get('[data-class=job-table-row]')
          .find('[data-class=job-status-failed]')
          .should('exist');
        });
      });
    });
  });
});
