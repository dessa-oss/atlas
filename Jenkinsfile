def build_number = env.BUILD_URL
def customMetrics = [:]
def customMetricsMap = [:]

pipeline{
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
        stage('Install Test Requirements') {
            steps {
                container("python3") {
                    sh "pip install -r requirements_test.txt"
                }
            }
        }
        stage('Build Atlas Wheels') {
            steps {
                container("python3") {
                    sh "./devops/build_scripts/build_all_dev.sh"
                }
            }
        }
        stage('Run Atlas Unit test and coverage'){
            failFast true
            parallel{
                stage('Run Unit Tests') {
                    steps {
                        container("python3") {
                            sh "./run_unit_tests.sh"
                        }
                    }
                }
                stage('Run Coverage Tests') {
                    steps {
                        container("python3") {
                            sh "./run_coverage_tests.sh unittest"
                        }
                    }
                }
            }
        }
        stage('Run Atlas Integration Tests and Prepare for Acceptance Tests'){
            parallel{
                stage("Integration Tests") {
                    stages{
                        stage('Run Integration Tests') {
                            steps {
                                container("python3") {
                                    sh './run_integration_tests.sh'
                                }
                            }
                        }
                        stage('Run Coverage Tests') {
                            steps {
                                container("python3") {
                                    sh "./run_coverage_tests.sh integration"
                                }
                            }
                        }
                    }
                }
                stage('Install Foundations (container 1)') {
                    steps {
                        container("python3-1") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'python -m pip install ../dist/*.whl'
                            }
                            dir("${WORKSPACE}/foundations_ui") {
                                sh "yarn install"
                            }
                        }
                    }
                }
                stage('Install Foundations (container 2)') {
                    steps {
                        container("python3-2") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'python -m pip install ../dist/*.whl'
                            }
                        }
                    }
                }
                stage('Install Foundations (container 3)') {
                    steps {
                        container("python3-3") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'python -m pip install ../dist/*.whl'
                            }
                        }
                    }
                }
                stage('Install Foundations (container 4)') {
                    steps {
                        container("python3-4") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'python -m pip install ../dist/*.whl'
                            }
                        }
                    }
                }
            }
        }
        stage('Acceptance Tests'){
            failFast true
            parallel{
                stage('Atlas Acceptance Tests') {
                    steps{
                        container("python3") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'cp -r ../testing/* . || true'
                                sh """export LOCAL_DOCKER_SCHEDULER_HOST=$ATLAS_LOCAL_SCHEDULER && \
                                        export REDIS_HOST=$ATLAS_LOCAL_SCHEDULER && \
                                        export EXECUTION_REDIS_HOST=localhost && \
                                        export EXECUTION_REDIS_PORT=6379 && \
                                        python -Wi -m unittest -f -v acceptance"""
                            }
                        }
                    }
                }
                stage('Atlas Acceptance Tests for Stageless Deploys') {
                    steps {
                        container("python3-1") {
                            ws("${WORKSPACE}/atlas/testing") {
                                sh 'cp -r ../testing/* . || true'
                                sh 'python -Wi -m unittest -f -v stageless_acceptance'
                            }
                        }
                    }
                }
                stage('Atlas REST API Acceptance Tests') {
                    stages{
                        stage('Atlas REST API Acceptance Tests') {
                            steps {
                                container("python3-2") {
                                    dir("${WORKSPACE}"){
                                        sh "./devops/teardown_frontend_dev_atlas.sh || true"
                                        sh "./atlas/foundations_rest_api/src/foundations_rest_api/config/envsubst_local.sh"
                                        sh """export FOUNDATIONS_SCHEDULER_HOST=$ATLAS_LOCAL_SCHEDULER && \
                                            cd atlas/foundations_rest_api/src && \
                                            ./foundations_rest_api/config/job_submission_envsubst.sh"""
                                    }
                                    dir("${WORKSPACE}/atlas/foundations_rest_api/src") {
                                        sh """export FOUNDATIONS_HOME=`pwd`/acceptance/v2beta/fixtures/remote_foundations_home && \
                                                export AUTH_CLIENT_CONFIG_PATH=`pwd`/foundations_rest_api/config/auth_client_config.yaml && \
                                                export REDIS_URL=redis://${ATLAS_LOCAL_SCHEDULER}:5556 && \
                                                python -Wi -m unittest -f -v acceptance"""
                                        sh "../../../devops/teardown_frontend_dev_atlas.sh || true"
                                    }
                                }
                            }
                        }
                        stage('Atlas Auth Acceptance Tests'){
                            steps {
                                container("python3-2") {
                                    dir("${WORKSPACE}") {
                                        sh "./devops/teardown_frontend_dev_atlas.sh || true"
                                        sh "./atlas/foundations_rest_api/src/foundations_rest_api/config/envsubst_local.sh"
                                        sh """export AUTH_CLIENT_CONFIG_PATH=`pwd`/atlas/foundations_rest_api/src/foundations_rest_api/config/auth_client_config.yaml && \
                                                export REDIS_PORT=6379 && \
                                                export FOUNDATIONS_SCHEDULER_URL=http://$ATLAS_LOCAL_SCHEDULER:5000 && \
                                                export FOUNDATIONS_HOME=`pwd`/atlas/testing/auth_acceptance/foundations_home && \
                                                python ./devops/startup_atlas_api.py 37722 &"""
                                    }
                                    ws("${WORKSPACE}/atlas/testing") {
                                        sh 'cp -r ../testing/* . || true'
                                        sh """export AUTH_CLIENT_CONFIG_PATH=/home/jenkins/agent/workspace/foundations_master/foundations_rest_api/src/foundations_rest_api/config/auth_client_config.yaml && \
                                                export REDIS_URL=redis://${ATLAS_LOCAL_SCHEDULER}:5556 && \
                                                python -Wi -m unittest -f -v auth_acceptance"""
                                        sh "../../devops/teardown_frontend_dev_atlas.sh || true"
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Run Atlas Cypress Tests') {
                    steps {
                        container("python3-1") {
                            // dir("${WORKSPACE}") {
                            //     sh "mkdir -p ~/.foundations/logs"
                            //     sh "./foundations_rest_api/src/foundations_rest_api/config/envsubst_local.sh"
                            //     sh """export FOUNDATIONS_SCHEDULER_URL=http://${ATLAS_LOCAL_SCHEDULER}:5000 && \
                            //             export REDIS_HOST=$ATLAS_LOCAL_SCHEDULER && \
                            //             export REDIS_PORT=5556 && \
                            //             export REDIS_URL=redis://${ATLAS_LOCAL_SCHEDULER}:5556 && \
                            //             export AUTH_CLIENT_CONFIG_PATH=`pwd`/foundations_rest_api/src/foundations_rest_api/config/auth_client_config.yaml && \
                            //             python `pwd`/devops/startup_atlas_api.py 8000 &"""
                            //     sh "`pwd`/devops/build_scripts/helpers/wait_for_url.sh 'http://localhost:8000/api/v2beta/projects' 30"
                            //     sh """export REACT_APP_API_STAGING_URL='http://localhost:8000/api/v2beta/' && \
                            //             cd foundations_ui && \
                            //             BROWSER=none PORT=8082 npm start &"""
                            //     sh "`pwd`/devops/build_scripts/helpers/wait_for_url.sh 'http://localhost:8082' 30"
                            //     sh "sleep 60"
                            //     sh """export CYPRESS_LOCAL_FOUNDATIONS_HOME=`pwd`/foundations_ui/cypress/fixtures/atlas_scheduler/.foundations && \
                            //             export CYPRESS_SCHEDULER_IP=$ATLAS_LOCAL_SCHEDULER && \
                            //             export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=$REMOTE_FOUNDATIONS_HOME && \
                            //             export CYPRESS_SCHEDULER_REDIS_PORT=5556 && \
                            //             export CYPRESS_GUI_HOST=localhost && \
                            //             export CYPRESS_GUI_PORT=8082 && export CYPRESS_ATLAS_EDITION=CE && \
                            //             export CYPRESS_PROXY_PORT=5558 && \
                            //             export CYPRESS_REST_API_HOST=localhost && \
                            //             export CYPRESS_REST_API_PORT=8000 && \
                            //             export CYPRESS_FAIL_FAST=true && \
                            //             export AUTH_CLIENT_CONFIG_PATH=`pwd`/foundations_rest_api/src/foundations_rest_api/config/auth_client_config.yaml && \
                            //             cd foundations_ui && \
                            //             npm run cy:run --"""
                            // }
                        }
                    }
                }
            }
        }
        stage('UI Test for Atlas'){
            parallel{
                stage('UI Test for Atlas') {
                    stages {
                        stage('Install dependencies for Atlas UI') {
                            steps {
                                container("python3") {
                                    ws("${WORKSPACE}/foundations_ui/") {
                                        sh "yarn cache clean"
                                        sh "yarn install"
                                    }
                                }
                            }
                        }
                        stage('Check for Atlas linting ') {
                            steps {
                                container("python3") {
                                    ws("${WORKSPACE}/foundations_ui/") {
                                        sh "node_modules/.bin/eslint ."
                                    }
                                }
                            }
                        }
                    }
                }

            }
        
        }
        stage('Upload Coverage results to Jenkins') {
            steps {
                container("python3") {
                    sh "tar -czvf coverage.tar.gz atlas/coverage_results"
                    archiveArtifacts artifacts: 'coverage.tar.gz'
                }
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
        stage('Trigger Build Artifacts for Atlas Pipeline') {
            when{
                branch 'master'
            }
            steps {
                container("python3") {
                    script {
                        echo "Triggering job for building Atlas Artifacts"
                        f9s_commit_hash = sh(script: "echo \$(git log --pretty=format:'%h' -n 1)", returnStdout: true).trim()
                        println("Attempting to trigger pipeline with version of ${f9s_commit_hash}")
                        build job: "build-artifacts-atlas", wait: false, parameters: [
                            [$class: 'StringParameterValue', name: 'f9s_commit_hash', value: "${f9s_commit_hash}"]
                        ]
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
            influxDbPublisher selectedTarget: 'foundations', customPrefix: 'foundations', customProjectName: 'foundations', jenkinsEnvParameterField: '', jenkinsEnvParameterTag: '', customDataMap: customMetricsMap
        }
        failure {
            script {
                def output_logs = String.join('\n', currentBuild.rawBuild.getLog(200))
                def attachments = [
                    [
                        pretext: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                        text: output_logs,
                        fallback: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.',
                        color: '#FF0000'
                    ]
                ]

                slackSend(channel: '#f9s-builds', attachments: attachments)
            }
        }
        success {
            slackSend color: '#00FF00', message: 'Build succeeded for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.'
        }
        cleanup {
            container("python3-1") {
                sh "`pwd`/devops/teardown_frontend_dev_atlas.sh || true"
                sh "kill -9 `lsof -i:8000 -t` || true"
                sh "kill -9 `lsof -i:8082 -t` || true"
            }
            container("python3-2") {
                sh "kill -9 `lsof -i:37722 -t` || true"
            }
            container("python3-3") {
                sh "kill -9 `lsof -i:8081 -t` || true"
            }
            container('python3') {
                sh 'rm -rf ci'
                sh 'git clean -fdx'
            }
        }
    }
}