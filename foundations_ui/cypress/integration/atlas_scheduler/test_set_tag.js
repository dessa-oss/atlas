describe('Test Set Tag', () => {
  const projectName = 'set_tag_project';
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  before(() => {
    cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
    cy.exec(`export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/set_tag/${projectName} && python main.py`);
  });

  beforeEach(() => {
    cy.visit(`http://${guiHost}:${guiPort}/projects`);
  });

  it('Project exists', () => {
    cy.contains(projectName).should('exist');
  });

  it('Tags exist on projects page', () => {
    cy.contains('[data-class=project-summary]', projectName)
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
  });

  it('Tags exist on project page', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=project-page-tags]')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('Tags exist on details modal', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=job-details-button]').click({ force: true });
      cy.get('[data-class=job-details-tags]')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('First two tags exist in job row', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('[data-class=metric-cell-tags]')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('not.contain', 'Float')
        .should('not.contain', 'None');
    });
  });

  it('Tags exist in job row hover', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.contains('[data-class=metric-cell-tags]', '...').trigger('mouseover', { force: true });
      cy.get('[data-class=hover-cell-tags-details]')
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
    });
  });
});
