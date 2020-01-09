describe.skip('Test Data Contract Info', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/projects');
    cy.contains('test').click({ force: true });
    cy.get('.icon-monitor').click({ force: true });
    cy.get('.validation-results-table-row').first().click({ force: true });
  });

  it('Has Button', () => {
    cy.get('.i--icon-open').should('exist');
  });

  it('Clicking Button Opens Modal', () => {
    cy.get('[data-cy=data-contract-info-modal').should('not.exist');
    cy.get('.i--icon-open').click({ force: true });
    cy.get('[data-cy=data-contract-info-modal').should('exist');
  });
});
