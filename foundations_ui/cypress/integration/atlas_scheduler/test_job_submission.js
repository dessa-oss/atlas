describe('Test Job Submission', () => {
  const schedulerIP = Cypress.env('SCHEDULER_IP');
  const schedulerRedisPort = Cypress.env('SCHEDULER_REDIS_PORT');
  const guiHost = Cypress.env('GUI_HOST');
  const guiPort = Cypress.env('GUI_PORT');

  const projectNames = ['job_submission_project', 'job_submission_project_with_foundations'];

  const states = projectNames.reduce((currArr, projectName) => {
    return currArr.concat([
      {
        testName: `Test Job Submission with CLI with project ${projectName}: current working directory outside job directory, relative path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit --debug scheduler ${projectName} main.py 0 "Complete_Task_1" dummy`,
      },
      {
        testName: `Test Job Submission with CLI with project ${projectName}: current working directory outside job directory, absolute path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler \`pwd\`/${projectName} main.py 0 "Complete_Task_2" dummy`,
      },
      {
        testName: `Test Job Submission with CLI with project ${projectName}: current working directory inside job directory, relative path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler . main.py 0 "Complete_Task_3" dummy`,
      },
      {
        testName: `Test Job Submission with CLI with project ${projectName}: current working directory inside job directory, absolute path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && foundations submit scheduler \`pwd\` main.py 0 "Complete_Task_4" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory outside job directory, script outside job directory, relative path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations login http://${schedulerIP}:5558 -u test -p test && python submit.py ${projectName} 0 "Complete_in 5" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory outside job directory, script outside job directory, absolute path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/ && foundations login http://${schedulerIP}:5558 -u test -p test && python submit.py \`pwd\`/${projectName} 0 "Complete_Task_6" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory inside job directory, script outside job directory, relative path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && python ../submit.py . 0 "Complete_Task_7" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory inside job directory, script outside job directory, absolute path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && python ../submit.py \`pwd\` 0 "Complete_Task_8" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory outside job directory, script inside job directory, relative path to job directory, relative path to script`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission && foundations login http://${schedulerIP}:5558 -u test -p test && python ${projectName}/submit.py ${projectName} 0 "Complete_Task_9" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory outside job directory, script inside job directory, relative path to job directory, absolute path to script`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission && foundations login http://${schedulerIP}:5558 -u test -p test && python \`pwd\`/${projectName}/submit.py ${projectName} 0 "Complete_Task_10" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory inside job directory, script inside job directory, relative path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && python submit.py . 0 "Complete_Task_11" dummy`,
      },
      {
        testName: `Test Job Submission with SDK with project ${projectName}: current working directory inside job directory, script inside job directory, absolute path to job directory`,
        projectName: projectName,
        command: `export FOUNDATIONS_HOME=\`pwd\`/cypress/fixtures/atlas_scheduler/.foundations && cd cypress/fixtures/atlas_scheduler/job_submission/${projectName} && foundations login http://${schedulerIP}:5558 -u test -p test && python submit.py \`pwd\` 0 "Complete_Task_12" dummy`,
      },
    ]);
  }, []);

  states.forEach(state => {
    describe(state.testName, () => {
      before(() => {
        cy.exec(`redis-cli -h ${schedulerIP} -p ${schedulerRedisPort} flushall`);
        cy.request('GET', `http://${guiHost}:${guiPort}/api/v2beta/cli_login`, {
          headers: { Authorization: 'Basic dGVzdDp0ZXN0Cg==' },
        });
        cy.exec(state.command);
      });

      beforeEach(() => {
        cy.visit(`http://${guiHost}:${guiPort}/projects`);
      });

      it('Project exists', () => {
        cy.contains(state.projectName).should('exist');
      });

      it('Job exists on projects page', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]').should('exist');
        });
      });

      it('Job is completed', () => {
        cy.contains(state.projectName).click({ force: true }).then(() => {
          cy.get('[data-class=job-table-row]')
            .find('[data-class=job-status-completed]')
            .should('exist');
        });
      });
    });
  });
});
