describe.skip('Test Nested Jobs', () => {  // wait_for_deployment_to_complete doesn't seem to work properly with nested jobs from remote deployments; unskip this when the pipeline is properly built
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const loginCommand = `foundations login http://${schedulerIP}:5558 -u test -p test`

  const projectName = 'nested_jobs_project';
  const command = `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && ${loginCommand} && cd cypress/fixtures/atlas_scheduler/nested_jobs/ && foundations submit scheduler ${projectName} main.py`;

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

  it('Two jobs exist on projects page', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-table-row]').should('have.length', 2);
    });
  });

  it('All jobs are completed', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-table-row]')
      .find('[data-class=job-status-completed]')
      .should('have.length', 2);
    });
  });

  it.only('Jobs have proper metrics', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-table-cell-with-header-name]').should('contain', 'job1');
      cy.get('[data-class=job-table-cell-with-header-name]').should('contain', 'job2');
    });
  });
});
