before(() => {
  cy.exec('python cypress/fixtures/atlas_scheduler/envsubst.py');

  // if (Cypress.env('FAIL_FAST')) {
  //   cy.task('shouldSkip').then(value => {
  //     if (value) {
  //       this.skip();
  //     }
  //   });
  // }
});

beforeEach(() => {
  // if (Cypress.env('FAIL_FAST')) {
  //   cy.task('shouldSkip').then(value => {
  //     if (value) {
  //       this.skip();
  //     }
  //   });
  // }

  // const guiHost = Cypress.env('GUI_HOST');
  const restApiHost = Cypress.env('REST_API_HOST') || Cypress.env('GUI_HOST');
  // const proxyPort = Cypress.env('PROXY_PORT');
  const restApiPort = Cypress.env('REST_API_PORT') || Cypress.env('PROXY_PORT');

  cy.request({
    url: `http://${restApiHost}:${restApiPort}/api/v2beta/auth/cli_login`,
    headers: { Authorization: 'Basic dGVzdDp0ZXN0' },
  })
    .then(response => {
      cy.setCookie('atlas_access_token', response.body.access_token);
      cy.setCookie('atlas_refresh_token', response.body.refresh_token);
    });
});

// afterEach(() => {
//   if (this.currentTest.state === 'failed') {
//     return cy.task('shouldSkip', true);
//   }
// });
