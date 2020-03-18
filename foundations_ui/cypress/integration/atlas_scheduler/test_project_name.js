describe('Test Project Name', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');
  const atlasRestAPIPort = Cypress.env('ATLAS_REST_API_PORT');


  const states = [
    {
      testName: 'Test Project Name Option through CLI',
      projectName: 'project_name',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python -m foundations submit scheduler --project-name project_name job_project main.py 1`,
    },
    {
      testName: 'Test Normal CLI Job Submission',
      projectName: 'project_name_project',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python -m foundations submit scheduler project_name_project main.py 2`,
    },
    {
      testName: 'Test Job Config Project Name through CLI',
      projectName: 'project_name_with_job_config',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python -m foundations submit scheduler with_job_config_project main.py 3`,
    },
    {
      testName: 'Test Override Job Config Project Name with Option through CLI',
      projectName: 'project_name_with_override_option',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python -m foundations submit scheduler --project-name project_name_with_override_option with_job_config_project main.py 4`,
    },
    {
      testName: 'Test Normal SDK Job Submission',
      projectName: 'project_name',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python project_name_project/main.py 5`,
    },
    {
      testName: 'Test Normal SDK Job Submission with Job Config from Outside Job Directory',
      projectName: 'project_name',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python with_job_config_project/main.py 6`,
    },
    {
      testName: 'Test Normal SDK Job Submission with Job Config from Within Job Directory',
      projectName: 'with_job_config_project',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name/with_job_config_project && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python main.py 7`,
    },
    {
      testName: 'Test SDK Job Submission with Job Directory and Project Name Parameters',
      projectName: 'project_name',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name/ && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python submit.py --job-directory=job_project --project-name=project_name main.py 8`,
    },
    {
      testName: 'Test SDK Job Submission with Job Directory Parameter',
      projectName: 'project_name_project',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name/ && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python submit.py --job-directory=project_name_project main.py 9`,
    },
    {
      testName: 'Test SDK Job Submission with Job Directory and Project Name Parameters and Job Config',
      projectName: 'project_name',
      command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/project_name/ && python -m foundations login http://${schedulerIP}:${atlasRestAPIPort} -u test -p test && python submit.py --job-directory=with_job_config_project --project-name=project_name main.py 10`,
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
        cy.contains(state.projectName).should('exist');
      });
    });
  });
});
