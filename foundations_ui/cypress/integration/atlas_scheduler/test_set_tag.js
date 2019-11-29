describe('Test Set Tag', () => {
  const projectName = 'set_tag_project';

  before(() => {
    cy.exec('redis-cli -h 54.91.54.99 -p 5556 flushall');
    cy.exec(`export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/set_tag/${projectName} && python main.py`);
  });

  beforeEach(() => {
    cy.visit('http://54.91.54.99:5555/projects');
  });

  it('Project exists', () => {
    cy.contains(projectName).should('exist');
  });

  it('Tags exist on projects page', () => {
    cy.contains('.project-summary-container', projectName)
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
  });

  it('Tags exist on project page', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('.project-summary-tags-container')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('Tags exist on details modal', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('.pop-up-cell').click({ force: true });
      cy.get('.container-tags')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('First two tags exist in job row', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.get('.type-tag')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('not.contain', 'Float')
        .should('not.contain', 'None');
    });
  });

  it('Tags exist in job row hover', () => {
    cy.contains(projectName).click({ force: true }).then(() => {
      cy.contains('.type-tag', '...').trigger('mouseover', { force: true });
      cy.get('.job-cell-hover')
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
    });
  });
});
