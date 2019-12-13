describe('Test Authentication', () => {
    const atlasEdition = Cypress.env('ATLAS_EDITION');

    if (atlasEdition === 'CE') {
        console.log('Skipping because ATLAS_EDITION is CE');
    } else if (atlasEdition === 'TEAM') {
        const guiHost = Cypress.env('GUI_HOST');
        const guiPort = Cypress.env('GUI_PORT');
        const page = `http://${guiHost}:${guiPort}`;
    
        it('test unsuccessful login does not have tokens', () => {
            cy.visit(page);
    
            cy.get('input[name=username]').type('asdf', {force: true});
            cy.get('input[name=password]').type('asdf', {force: true});
            cy.get('.login-submit').click({force: true});
    
            cy.getCookie('atlas_access_token').should('not.exist');
            cy.getCookie('atlas_refresh_token').should('not.exist');
        });
        
        it.only('test successful login redirects to projects page and has tokens', () => {
            cy.visit(page);
    
            cy.get('input[name=username]').type('test', {force: true});
            cy.get('input[name=password]').type('test', {force: true});
            cy.get('.login-submit').click({force: true});
            cy.wait(200);
    
            cy.get('.header-link-container a[href="/projects"]').click({force: true});
    
            cy.url().should('include', '/projects');
            cy.getCookie('atlas_access_token').should('exist');
            cy.getCookie('atlas_refresh_token').should('exist');
        });
    }
});
