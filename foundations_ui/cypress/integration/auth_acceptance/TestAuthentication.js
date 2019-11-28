describe('Test Authentication', function() {

    const page = 'http://54.84.19.116:5555'

    it('test unsuccessful login does not have tokens', function() {
        cy.visit(page)

        cy.get('input[name=username]').type('asdf', {force: true})
        cy.get('input[name=password]').type('asdf', {force: true})
        cy.get('.login-submit').click({force: true})

        cy.getCookie('atlas_access_token').should('not.exist')
        cy.getCookie('atlas_refresh_token').should('not.exist')
    })
    
    it('test successful login redirects to projects page and has tokens', function() {
        cy.visit(page)

        cy.get('input[name=username]').type('test', {force: true})
        cy.get('input[name=password]').type('test', {force: true})
        cy.get('.login-submit').click({force: true})
        cy.wait(200)

        cy.get('.header-link-container a[href="/projects"]').click({force: true})

        cy.url().should('include', '/projects')
        cy.getCookie('atlas_access_token').should('exist')
        cy.getCookie('atlas_refresh_token').should('exist')
    })
})