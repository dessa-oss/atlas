describe('Test Artifact Saving', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const states = [
    {
      testName: 'Test Artifact Saving through the CLI',
      projectName: 'artifact_saving_project',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && foundations login http://${schedulerIP}:5558 -u test -p test && cd cypress/fixtures/atlas_scheduler/artifact_saving && foundations submit scheduler artifact_saving_project main.py`,
    },
    {
      testName: 'Test Artifact Saving through the SDK',
      projectName: 'artifact_saving_project',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && foundations login http://${schedulerIP}:5558 -u test -p test && cd cypress/fixtures/atlas_scheduler/artifact_saving/artifact_saving_project && python main.py`,
    },
  ];

  const artifactNames = [
    'fan-man.png', 'ICQ Uh Oh.mp3', 'dogge.mp4', 'cat.gif', 'wilhelm.wav',
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

      it('Job is completed', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find('[data-class=job-status-completed]')
            .should('exist');
        });
      });

      it('Artifacts exist', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-details-button]').click({ force: true });
          cy.get('[data-class=artifacts-tab-button]').click({ force: true });
          artifactNames.forEach(artifact => {
            cy.get('[data-class=artifacts-table-row]').should('contain', artifact);
          });
        });
      });
    });
  });
});
