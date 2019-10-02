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
                    git branch: 'trunk', credentialsId: 'devops', url: 'git@github.com:DeepLearnI/foundations.git'
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
        stage('Foundations Install Test Requirements') {
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
        stage('Run Unit Tests') {
            steps {
                container("python3") {
                    sh "./run_unit_tests.sh"
                }
            }
        }
        stage('Build Model Package Image and Push to Testing Env') {
            steps {
                container("python3") {
                    ws("${WORKSPACE}/foundations_model_package/src"){
                        sh 'docker login docker.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                        sh 'docker login docker-staging.shehanigans.net -u $NEXUS_USER -p $NEXUS_PASSWORD'
                        sh './build.sh'
                        sh 'docker push docker-staging.shehanigans.net/foundations-model-package:latest'
                        sh './pull_staging_image_onto_scheduler.sh'
                    }
                }
            }
        }
        stage('Run Integration Tests') {
            // options {
            //     lock('ingress-tests')
            // }
            steps {
                container("python3") {
                    sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && ./run_integration_tests.sh'
                }
            }
        }
        stage('Rebuild Python package using the wheels') {
            steps {
                container("python3") {
                    sh "./ci_install_requirements.sh"
                    sh 'python -m pip install ./dist/*.whl'
                }
            }
        }
        stage('Python3 All Foundations Acceptance Tests'){
            failFast true
            parallel{
                stage('Parallel Foundations Acceptance Tests') {
                    stages {
                        stage('Python3 Foundations Acceptance Tests'){
                            // options {
                            //     lock('ingress-tests')
                            // }
                            steps{
                                container("python3") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                        sh 'cp -r ../testing/* . || true'
                                        sh "python -Wi -m unittest -f -v acceptance"
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Acceptance Tests for Stageless Deploys') {
                    stages{
                        stage('Parallel Foundations Acceptance Tests for Stageless Deploys'){
                            steps {
                                container("python3-1") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'python -Wi -m unittest -f -v stageless_acceptance'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Scheduler Acceptance Tests for Remote Deploys') {
                    stages{
                        stage('Python3 Foundations Scheduler Acceptance Tests for Remote Deploys') {
                            steps {
                                container("python3-2") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && python -Wi -m unittest -f -v scheduler_acceptance'
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations REST API Acceptance Tests') {
                    stages{
                        stage('Python3 Foundations REST API Acceptance Tests') {
                            steps {
                                container("python3-3") {
                                    ws("${WORKSPACE}/foundations_rest_api/src") {
                                        sh 'python -m pip install ../../dist/*.whl'
                                        sh "python -Wi -m unittest -f -v acceptance"
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Parallel Foundations Orbit Acceptance Tests') {
                    stages{
                        stage('Python3 Foundations Orbit Acceptance Tests') {
                            // options {
                            //     lock('ingress-tests')
                            // }
                            steps {
                                container("python3-4") {
                                    ws("${WORKSPACE}/testing") {
                                        sh 'python -m pip install ../dist/*.whl'
                                        sh 'cp -r ../testing/* . || true'
                                        sh 'export FOUNDATIONS_SCHEDULER_HOST=$FOUNDATIONS_SCHEDULER_ACCEPTANCE_HOST && python -Wi -m unittest -f -v orbit_acceptance'
                                    }
                                }
                            }
                        }
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
        stage('Results') {
            steps {
                archiveArtifacts artifacts: '**/*.whl', fingerprint: true
            }
        }
    }
}