// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('forceClick', { prevSubject: 'element' }, element => cy.wrap(element).click({ force: true }));
Cypress.Commands.add('forceType', { prevSubject: 'element' }, (element, keys) => cy.wrap(element).type(keys, { force: true }));
Cypress.Commands.add('cyGet', dataClass => cy.get(`[data-class=${dataClass}]`));
Cypress.Commands.add('cyFind', { prevSubject: 'element' }, (element, dataClass) => cy.wrap(element).find(`[data-class=${dataClass}]`));
