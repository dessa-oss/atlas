
describe('Test Local Job Submission', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const states = [
    {
      testName: 'Test Local Job Submission with CLI from outside job directory',
      projectName: 'local_job_submission',
      command: 'export FOUNDATIONS_HOME=`pwd`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/local_job_submission/ && python local_job_submission_project/main.py 0 "Complete_Task_1" dummy',
    },
    {
      testName: 'Test Local Job Submission with CLI from inside job directory',
      projectName: 'local_job_submission_project',
      command: 'export FOUNDATIONS_HOME=`pwd`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/local_job_submission/local_job_submission_project && python main.py 0 "Complete_Task_2" dummy',
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

      it('Job exists on projects page', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]').should('exist');
        });
      });

      it('Job has failed', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find('[data-class=job-status-completed]')
            .should('exist');
        });
      });
    });
  });
});
