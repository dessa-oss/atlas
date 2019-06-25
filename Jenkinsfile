def build_number = env.BUILD_URL
def customMetrics = [:]
def customMetricsMap = [:]

pipeline {

    agent {
        label 'ci-pipeline-jenkins-slave'
    }
    stages {
        stage('Preparation') {
            steps {
                script {
                    customMetricsMap["jenkins_data"] = customMetrics
                    checkout scm
                }
            }
        }
        stage('Get Foundations Scheduler') {
            steps {
                container("python3") {
                    sh 'python -m pip install -U foundations-scheduler'
                }
                
            }
        }
        stage('Python3 Foundations Install Test Requirements') {
            steps {
                container("python3") {
                    sh "./ci_install_requirements.sh"
                }
            }
        }
        stage('Build Foundations Wheels') {
            steps {
                container("python3") {
                    sh "./build_dist.sh"
                }
            }
        }
        stage('Python3 Run Unit Tests') {
            steps {
                container("python3") {
                    sh "./run_unit_tests.sh"
                }
            }
        }
        stage('Python3 Run Integration Tests') {
            steps {
                container("python3") {
                    sh "./run_integration_tests.sh"
                }
            }
        }
        stage('Python3 Foundations Acceptance Tests') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/testing") {
                        sh "python -Wi -m unittest -f -v acceptance"
                    }
                }
            }
        }
        stage('Python3 Foundations Acceptance Tests for Stageless Deploys') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/testing") {
                        sh 'python -Wi -m unittest -f -v stageless_acceptance'
                    }
                }
            }
        }
        stage('Python3 Foundations Remote Acceptance Tests for Remote Deploys') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/testing") {
                        sh "python -Wi -m unittest -f -v remote_acceptance"
                    }
                }
            }
        }
        stage('Python3 Foundations Scheduler Acceptance Tests for Remote Deploys') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/testing") {
                        sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && python -Wi -m unittest -f -v scheduler_acceptance'
                    }
                }
            }
        }
        stage('Python3 Foundations REST API Acceptance Tests') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/foundations_rest_api/src") {
                        sh "python -Wi -m unittest -f -v acceptance"
                    }
                }
            }
        }
        stage('Install dependencies for Foundations UI') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "yarn install"
                    }
                }
            }
        }
        stage('Run Front End Unit Tests') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "yarn run test"
                    }
                }
            }
        }
        stage('Check for linting') {
            steps {
                container("yarn") {
                    ws("${WORKSPACE}/foundations_ui/") {
                        sh "node_modules/.bin/eslint ."
                    }
                }
            }
        }
        stage('Upload Wheels to Releases') {
            steps {
                container("python3"){
                    sh "./upload_modules_to_artifactory.sh $NEXUS_PYPI"
                }
            }
        }
        stage('Build GUI and Rest API Images'){
            steps {
                container("python3"){
                    sh "./build_gui.sh"
                }
            }
        }
        stage('Push GUI and Rest API Images'){
            steps {
                container("python3"){
                    sh "./push_gui_images.sh"
                }
            }
        }
        stage('Results') {
            steps {
                archiveArtifacts artifacts: '**/*.whl', fingerprint: true
            }
        }
        stage("Calculate Recovery Metrics") {
            steps {
                script {
                    def last_build = currentBuild.getPreviousBuild()
                    def last_failed_build
                    def current_time = System.currentTimeMillis()
                    
                    while(last_build != null && last_build.result == "FAILURE") {
                        last_failed_build = last_build
                        last_build = last_build.getPreviousBuild()
                    }
                    
                    if(last_failed_build != null) {
                        time_to_recovery = current_time - last_failed_build.getTimeInMillis() 
                        customMetrics["time_to_recovery"] = time_to_recovery
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                customMetricsMap["jenkins_data"] = customMetrics
            }
            influxDbPublisher customPrefix: 'foundations', customProjectName: 'foundations', jenkinsEnvParameterField: '', jenkinsEnvParameterTag: '', customDataMap: customMetricsMap
        }
        failure {
            script {
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
            }
        }
        success {
            slackSend color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.'
        }
    }
}
