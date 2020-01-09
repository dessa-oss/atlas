describe('Test Monitor and Job', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const projectName = `my_project${Math.floor(Math.random() * 100)}`;
  const monitorName = `my_monitor${Math.floor(Math.random() * 100)}`;

  before(() => {
    cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
    cy.visit(`http://${guiHost}:${guiPort}/projects`);

    cy.request('GET', `http://${guiHost}:${guiPort}/api/v2beta/cli_login`, {
      headers: { Authorization: 'Basic dGVzdDp0ZXN0Cg==' },
    });

    cy.exec(`export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/orbit_acceptance/.foundations && foundations login -u test -p test http://${schedulerIP}:5558 && cd cypress/fixtures/orbit_acceptance/my_project/ && foundations monitor create --name=${monitorName} --project_name=${projectName} . validate.py`);
  });

  beforeEach(() => {
    cy.visit(`http://${guiHost}:${guiPort}/projects`);
  });

  it('Project exists', () => {
    cy.contains(projectName).should('exist');
  });

  it('Monitor exists', () => {
    cy.contains(projectName).forceClick().then(() => {
      cy.cyGet('monitor-name').should('contain', monitorName);
    });
  });

  it.only('Monitor can be scheduled', () => {
    cy.contains(projectName).forceClick()
    // Schedule jobs with the monitor and run one
      .then(() => {
        cy.cyGet('monitor-name')
          .within(() => {
            cy.contains(monitorName).forceClick();
          })
          .then(() => {
            cy.cyGet('repeat-unit').find('input').forceType('minute{enter}');
            cy.cyGet('repeat-on').find('input').forceType('0{enter}15{enter}30{enter}45{enter}');

            cy.get('.end-time').forceClick().then(() => {
              cy.get('.flatpickr-calendar.open')
                .find('.flatpickr-minute')
                .siblings('.arrowUp')
                .forceClick();
            });
          })
          .then(() => {
            cy.get('[data-class=save-schedule]:not(.disabled)').forceClick()
              .then(() => cy.cyGet('status').should('contain', 'Active'));
          });
      })
    // Wait for a job to complete and pause the monitor
      .then(() => {
        cy.wait(15000);
        cy.cyGet('refresh-job-table').forceClick()
          .then(() => cy.cyGet('monitor-job-table-row').should('exist'))
          .then(() => {
            cy.cyGet('pause-button').forceClick()
              .then(() => cy.cyGet('status').should('contain', 'Paused'));
          });
      })
    // Check that a validation report exists
      .then(() => {
        cy.cyGet('data-health-tab').forceClick()
          .then(() => {
            cy.contains('Data Validation Results').should('exist');
            cy.contains(monitorName).should('exist');
          });
      })
    // Check that a metric exists
      .then(() => {
        cy.cyGet('model-metrics-tab').forceClick()
          .then(() => cy.cyGet('metric-chart').should('exist'));
      });
  });
});
