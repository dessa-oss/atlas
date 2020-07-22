describe('Test Log Param', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const projectName = 'log_param_project';

  const states = [
    {
      testName: 'Test Logging Params of Type Int',
      projectName: projectName,
      params: [
        {
          label: 'param_int',
          value: '1',
          hasHover: false,
        },
        {
          label: 'param_large_int',
          value: '8.8889e+24',
          hasHover: false,
        },
        {
          label: 'param_list_of_ints',
          value: '[1, 2]',
          hasHover: false,
        },
        {
          label: 'param_long_list_of_ints',
          value: '[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]',
          hasHover: true,
        },
        {
          label: 'param_long_list_of_long_ints',
          value: '[8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24, 8.888888888888889e+24]',
          hasHover: true,
        },
        {
          label: 'param_mixed_type',
          value: '1',
          hasHover: false,
        },
        {
          label: 'param_repeat',
          value: '19',
          hasHover: false,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_param/ && python -m foundations login http://${schedulerIP}:5558 -u test -p test && python -m foundations submit scheduler ${projectName} ints.py`,
    },
    {
      testName: 'Test Logging Params of Type Float',
      projectName: projectName,
      params: [
        {
          label: 'param_float',
          value: '1',
          hasHover: false,
        },
        {
          label: 'param_large_float',
          value: '1.0000e+9',
          hasHover: false,
        },
        {
          label: 'param_list_of_floats',
          value: '[1, 2]',
          hasHover: false,
        },
        {
          label: 'param_long_list_of_floats',
          value: '[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]',
          hasHover: true,
        },
        {
          label: 'param_long_list_of_long_floats',
          value: '[999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888, 999999999.8888888]',
          hasHover: true,
        },
        {
          label: 'param_mixed_type',
          value: '2.222',
          hasHover: false,
        },
        {
          label: 'param_repeat',
          value: '6.3333',
          hasHover: false,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_param/ && python -m foundations login http://${schedulerIP}:5558 -u test -p test && python -m foundations submit scheduler ${projectName} floats.py`,
    },
    {
      testName: 'Test Logging Params of Type Str',
      projectName: projectName,
      params: [
        {
          label: 'param_str',
          value: '1',
          hasHover: false,
        },
        {
          label: 'param_long_str',
          value: 'asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf',
          hasHover: true,
        },
        {
          label: 'param_long_list_of_str',
          value: '[qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe, qwe]',
          hasHover: true,
        },
        {
          label: 'param_mixed_type',
          value: 'asdf',
          hasHover: false,
        },
        {
          label: 'param_repeat',
          value: 'str19',
          hasHover: false,
        },
      ],
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/log_param/ && python -m foundations login http://${schedulerIP}:5558 -u test -p test && python -m foundations submit scheduler ${projectName} strs.py`,
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

      it('Project has param headers', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.params.map(param => param.label).forEach(paramName => {
            cy.get('[data-class=param-header]')
              .should('contain', paramName);
          });
        });
      });

      it('Job has param values', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.params.forEach(param => {
            cy.get(`[data-class=job-table-cell-with-header-${param.label}]`)
              .should('contain', param.value);
          });
        });
      });

      it('Job hover has param values', () => {
        cy.contains(projectName).click({ force: true }).then(() => {
          state.params.forEach(param => {
            if (param.hasHover) {
              cy.get(`[data-class=job-table-cell-with-header-${param.label}]`).trigger('mouseover', { force: true });
              cy.get('[data-class=hover-cell]').should('contain', param.value);
            }
          });
        });
      });
    });
  });
});
