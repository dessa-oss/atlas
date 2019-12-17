
const command_to_run = {
    testName: `Test Local Job Submission with CLI from outside job directory`,
    projectName: 'local_job_submission',
    command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/local_job_submission/ && python local_job_submission_project/main.py 0 "Complete_Task_1" dummy`
}

const schedulerIP = Cypress.env('SCHEDULER_IP');
const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
const guiHost = Cypress.env('GUI_HOST');
const guiPort = Cypress.env('GUI_PORT');

before(() => {
    cy.exec('python cypress/fixtures/atlas_scheduler/envsubst.py');
    cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
    cy.exec(command_to_run.command);
    cy.visit(`http://${guiHost}:${guiPort}/projects`);
    cy.contains(command_to_run.projectName).should('exist');
});


beforeEach(() => {
  if (Cypress.env('ATLAS_EDITION') === 'TEAM') {
    const schedulerIP = Cypress.env('SCHEDULER_IP');
    cy.exec(`foundations login http://${schedulerIP}:5558 -u test -p test`);
  }
});
