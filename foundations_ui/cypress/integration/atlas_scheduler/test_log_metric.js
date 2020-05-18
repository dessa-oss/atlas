describe('Test Log Metric', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const projectName = 'log_metric_project';

  const states = [
    {
      testName: 'Test Logging Metrics of Type Int',
      projectName: projectName,
      metrics: [
        {
          label: 'metric_int',
          value: '1',
          hasHover: false,
        },
        {
          label: 'metric_large_int',
          value: '8.8889e+24',
          hasHover: false,
        },
        {
          label: 'metric_list_of_ints',
          value: '[1, 2]',
          hasHover: false,
        },
        {
          label: 'metric_long_list_of_ints',
          value: '[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]',
          hasHover: true,
        },
        {
          label: 'metric_long_list_of_long_ints',
          value: '[8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24]',
          hasHover: true,
        },
        {
          label: 'metric_mixed_type',
          value: '1',
          hasHover: false,
        },
        {
          label: 'metric_repeat',
          value: '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]',
          hasHover: true,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_metric/ && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler ${projectName} ints.py`,
    },
    {
      testName: 'Test Logging Metrics of Type Float',
      projectName: projectName,
      metrics: [
        {
          label: 'metric_float',
          value: '1',
          hasHover: false,
        },
        {
          label: 'metric_large_float',
          value: '1.0000e+9',
          hasHover: false,
        },
        {
          label: 'metric_list_of_floats',
          value: '[1, 2]',
          hasHover: false,
        },
        {
          label: 'metric_long_list_of_floats',
          value: '[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]',
          hasHover: true,
        },
        {
          label: 'metric_long_list_of_long_floats',
          value: '[999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888]',
          hasHover: true,
        },
        {
          label: 'metric_mixed_type',
          value: '2.222',
          hasHover: false,
        },
        {
          label: 'numpy_value',
          value: '5.0',
          hasHover: false,
        },
        {
          label: 'metric_repeat',
          value: '[0, 0.3333333333333333, 0.6666666666666666, 1, 1.3333333333333333, 1.6666666666666667, 2, 2.3333333333333335, 2.6666666666666665, 3, 3.3333333333333335, 3.6666666666666665, 4, 4.333333333333333, 4.666666666666667, 5, 5.333333333333333, 5.666666666666667, 6, 6.333333333333333]',
          hasHover: true,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_metric/ && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler ${projectName} floats.py`,
    },
    {
      testName: 'Test Logging Metrics of Type Str',
      projectName: projectName,
      metrics: [
        {
          label: 'metric_str',
          value: '1',
          hasHover: false,
        },
        {
          label: 'metric_long_str',
          value: 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf',
          hasHover: true,
        },
        {
          label: 'metric_long_list_of_str',
          value: '[qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe]',
          hasHover: true,
        },
        {
          label: 'metric_mixed_type',
          value: 'asdf',
          hasHover: false,
        },
        {
          label: 'metric_repeat',
          value: '[str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14, str15, str16, str17, str18, str19]',
          hasHover: true,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_metric/ && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler ${projectName} strs.py`,
    },
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
        cy.contains(projectName).should('exist');
      });

      it('Job exists on projects page', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]').should('exist');
        });
      });

      it('Project has metric headers', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.metrics.map(metric => metric.label).forEach(metricName => {
            cy.get('[data-class=metric-header]')
              .should('contain', metricName);
          });
        });
      });

      it('Job has metric values', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.metrics.forEach(metric => {
            cy.get(`[data-class=job-table-cell-with-header-${metric.label}]`)
              .should('contain', metric.value);
          });
        });
      });

      it('Job hover has metric values', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.metrics.forEach(metric => {
            if (metric.hasHover) {
              cy.get(`[data-class=job-table-cell-with-header-${metric.label}]`).trigger('mouseover', { force: true });
              cy.get('[data-class=hover-cell]').should('contain', metric.value);
            }
          });
        });
      });
    });
  });
});
