node {
    stage('Preparation') { // for display purposes
        checkout scm
    }    
    container("python2") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Python2 Foundations Install Requirements') {
                sh "python -m pip install PyYAML==3.13 dill==0.2.8.2 pandas==0.23.3 mock freezegun futures promise==2.2.1 redis==2.10.6"
            }
            ws("${WORKSPACE}/src") {
                stage('Python2 Foundations Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
                stage('Python2 Foundations Integration Tests') {
                    sh "python -Wi -m unittest integration"
                }
                stage('Python2 Foundations Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
            }
            stage('Python2 Foundations Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations-0.0.0-py2-none-any.whl"
            }
        }
        ws("${WORKSPACE}/ssh_utils/") {
            stage('Python2 SSH Install Requirements') {
                sh "python -m pip install pysftp"
            }
            ws("${WORKSPACE}/src") {
                stage('Python2 SSH Unit Tests'){
                    sh "python -Wi -m unittest test"
                }
            }
            stage('Python2 SSH Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_ssh-0.0.0-py2-none-any.whl"
            }
        }
        ws("${WORKSPACE}/gcp_utils/") {
            stage('Python2 GCP Install Requirements') {
                sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Python2 GCP Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_gcp-0.0.0-py2-none-any.whl"
            }
        }
        ws("${WORKSPACE}/foundations_rest_api/") {
            stage('Python2 REST API Install Requirements') {
                sh "python -m pip install flask flask-restful Flask-Cors"
            }
            ws("${WORKSPACE}/src") {
                stage('Python2 Foundations REST API Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
            }
            stage('Python2 Foundations REST API Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_rest_api-0.0.0-py2-none-any.whl"
            }
        }
    }
    container("python3") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Python3 Foundations Install Requirements') {
                sh "python -m pip install PyYAML==3.13 dill==0.2.8.2 pandas==0.23.3 mock freezegun futures promise==2.2.1 redis==2.10.6"
            }
            ws("${WORKSPACE}/src") {
                stage('Python3 Foundations Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
                stage('Python3 Foundations Integration Tests') {
                    sh "python -Wi -m unittest integration"
                }
                stage('Python3 Foundations Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
            }
            stage('Python3 Foundations Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations-0.0.0-py3-none-any.whl"
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
                sh "python -m pip install flask flask-restful Flask-Cors"
            }
            ws("${WORKSPACE}/src") {
                stage('Python3 Foundations REST API Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
            }
            stage('Python3 Foundations REST API Create Artifact') {
                sh "python setup.py sdist bdist_wheel && python -m pip install -U dist/foundations_rest_api-0.0.0-py3-none-any.whl"
            }
        }
    }
    container("yarn") {
        ws("${WORKSPACE}/foundations_ui/") {
            stage('Install dependencies for Foundation UI') {
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
}
