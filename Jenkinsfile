node {
    def build_number = env.BUILD_URL
    try {
        stage('Preparation') { // for display purposes
            checkout scm
        }
        container("python3") {
            stage('Get Foundations Scheduler') {
                ws("${WORKSPACE}/build_tmp/foundations_scheduler") {
                    git credentialsId: 'ja-devops-github', url: 'https://github.com/DeepLearnI/foundations-scheduler.git'
                    sh 'git checkout master'
                    sh 'export DO_NOT_BUILD_IMAGES=TRUE && ./build_sdk.sh'
                }
                sh 'rm -rf build_tmp'
            }

            stage('Python3 Foundations Install Test Requirements') {
                sh "./ci_install_requirements.sh"
                sh "./build_dist.sh"
                sh "./upload_modules_to_artifactory.sh"
            }
            stage('Python3 Run Unit Tests') {
                sh "./run_unit_tests.sh"
            }
            stage('Python3 Run Integration Tests') {
                sh "./run_integration_tests.sh"
            }
            ws("${WORKSPACE}/testing"){
                stage('Python3 Foundations Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
                stage('Python3 Foundations Acceptance Tests for Remote Deploys') {
                    sh "python -Wi -m unittest remote_acceptance"
                }
            }
            ws("${WORKSPACE}/foundations_rest_api/src") {
                stage('Python3 Foundations REST API Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
            }
        }
        container("yarn") {
            ws("${WORKSPACE}/foundations_ui/") {
                stage('Install dependencies for Foundations UI') {
                    sh "yarn install"
                }
                stage('Run Front End Unit Tests') {
                    sh "yarn run test"
                }
                stage('Check for linting') {
                    sh "node_modules/.bin/eslint ."
                }
            }
        }
        stage('Results') {
            archiveArtifacts artifacts: '**/*.whl', fingerprint: true
        }
    } catch (Exception error) {
        slackSend(color: '#FF0000', message: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.')
        throw error
    }
}
