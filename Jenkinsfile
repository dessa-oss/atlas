node {
    def build_number = env.BUILD_URL
    try {
        stage('Preparation') { // for display purposes
            checkout scm
        }
        container("python3") {
            stage('Get Foundations Scheduler') {
                sh 'python -m pip install -U foundations-scheduler'
            }
            stage('Python3 Foundations Install Test Requirements') {
                sh "./ci_install_requirements.sh"
            }
            stage('Build Foundations Wheels') {
                sh "./build_dist.sh"
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
                stage('Python3 Foundations Remote Acceptance Tests for Remote Deploys') {
                    sh "python -Wi -m unittest remote_acceptance"
                }
                stage('Python3 Foundations Scheduler Acceptance Tests for Remote Deploys') {
                    sh 'FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST python -Wi -m unittest scheduler_acceptance'
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
        container("python3"){
            stage('Upload Wheels to Releases') {
                sh "./upload_modules_to_artifactory.sh $NEXUS_PYPI"
            }
            stage('Build GUI and Rest API Images'){
                sh "./build_gui.sh"
            }
            stage('Push GUI and Rest API Images'){
                sh "./push_gui_images.sh"
            }
        }
        stage('Results') {
            archiveArtifacts artifacts: '**/*.whl', fingerprint: true
        }
        slackSend(color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.')
    } catch (Exception error) {
        def output_logs = String.join('\n', currentBuild.rawBuild.getLog(100))
        def attachments = [
            [
                pretext: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                text: output_logs,
                fallback: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                color: '#FF0000'
            ]
        ]
        slackSend(channel: '#foundations-builds', attachments: attachments)
        throw error
    }
}
