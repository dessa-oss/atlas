node {
    stage('Preparation') { // for display purposes
        checkout scm
    }    
    container("python2") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Python2 Foundations Install Requirements') {
                sh "python -m pip install PyYaml dill pandas mock freezegun"
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
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/ssh_utils/") {
            stage('Python2 SSH Install Requirements') {
                sh "python -m pip install pysftp"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Python2 SSH Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/gcp_utils/") {
            stage('Python2 GCP Install Requirements') {
                sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Python2 GCP Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
    }
    container("python3") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Python3 Foundations Install Requirements') {
                sh "python -m pip install PyYaml dill pandas mock freezegun"
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
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/ssh_utils/") {
            stage('Python3 SSH Install Requirements') {
                sh "python -m pip install pysftp"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Python3 SSH Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/gcp_utils/") {
            stage('Python3 GCP Install Requirements') {
                sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Python3 GCP Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
    }
    stage('Results') {
        archiveArtifacts artifacts: '**/*.whl', fingerprint: true
    }
}