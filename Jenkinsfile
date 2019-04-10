node {
    def build_number = env.BUILD_URL
    try {
        stage('Preparation') { // for display purposes
            checkout scm
        }
        container("python3") {
            stage('Python3 Foundations Install Test Requirements') {
                sh "python -m pip install -r test_requirements.txt"
                sh "./build_dist.sh"
                sh "./upload_modules_to_artifactory.sh"
            }
            ws("${WORKSPACE}/foundations_sdk/") {
                stage('Python3 Foundations Install Requirements') {
                    sh "python -m pip install PyYAML==3.13 dill==0.2.8.2 pandas==0.23.3 futures promise==2.2.1 redis==2.10.6"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 Foundations Unit Tests') {
                        sh "python -Wi -m unittest test"
                    }
                    stage('Python3 Foundations Integration Tests') {
                        sh "python -Wi -m unittest integration"
                    }
                }
                stage('Python3 Foundations Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/foundations_spec/") {
                stage('Python3 Foundations Spec Install Requirements') {
                    sh "python -m pip install mock==2.0.0 Faker==1.0.0"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 Foundations Spec Unit Tests') {
                        sh "python -Wi -m unittest test"
                    }
                }
                stage('Python3 Foundations Spec Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_spec-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/foundations_contrib/") {
                stage('Python3 Foundations Contrib Install Requirements') {
                    sh "python -m pip install PyYAML==3.13 dill==0.2.8.2 pandas==0.23.3 futures promise==2.2.1 redis==2.10.6"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 Foundations Contrib Unit Tests') {
                        sh "python -Wi -m unittest test"
                    }
                    stage('Python3 Foundations Contrib Integration Tests') {
                        sh "python -Wi -m unittest integration"
                    }
                }
                stage('Python3 Foundations Contrib Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_contrib-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/foundations_internal/") {
                stage('Python3 Foundations Internal Install Requirements') {
                    sh "python -m pip install PyYAML==3.13 dill==0.2.8.2 pandas==0.23.3 futures promise==2.2.1 redis==2.10.6"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 Foundations Internal Unit Tests') {
                        sh "python -Wi -m unittest test"
                    }
                    stage('Python3 Foundations Internal Integration Tests') {
                        sh "python -Wi -m unittest integration"
                    }
                }
                stage('Python3 Foundations Internal Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_internal-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/testing"){
                stage('Python3 Foundations Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
                stage('Python3 Foundations Acceptance Tests for Remote Deploys') {
                    sh "python -Wi -m unittest remote_acceptance"
                }
            }
            ws("${WORKSPACE}/ssh_utils/") {
                stage('Python3 SSH Install Requirements') {
                    sh "python -m pip install pysftp"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 SSH Unit Tests'){
                        sh "python -Wi -m unittest test"
                    }
                }
                stage('Python3 SSH Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_ssh-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/aws_utils/") {
                stage('Python3 AWS Install Requirements') {
                    sh "python -m pip install pysftp"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 AWS Unit Tests'){
                        sh "python -Wi -m unittest test"
                    }
                }
                stage('Python3 AWS Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_aws-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/gcp_utils/") {
                stage('Python3 GCP Install Requirements') {
                    sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
                }
                ws("${WORKSPACE}/src") {
                }
                stage('Python3 GCP Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_gcp-0.0.0-py3-none-any.whl"
                }
            }
            ws("${WORKSPACE}/foundations_rest_api/") {
                stage('Python3 REST API Install Requirements') {
                    sh "python -m pip install flask==1.0.2 flask-restful==0.3.6 Flask-Cors==3.0.6 Werkzeug==0.14.1"
                }
                ws("${WORKSPACE}/src") {
                    stage('Python3 Foundations REST API Unit Tests') {
                        sh "python -Wi -m unittest test"
                    }
                    stage('Python3 Foundations REST API Acceptance Tests') {
                        sh "python -Wi -m unittest acceptance"
                    }
                }
                stage('Python3 Foundations REST API Create Artifact') {
                    sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_rest_api-0.0.0-py3-none-any.whl"
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
        // slackSend(color: '#FF0000', message: '@channel Build failed for `' + env.JOB_NAME + '` please visit ' + env.BUILD_URL + ' for more details.')
        throw error
    }
}
