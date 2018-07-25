node {
    stage('Preparation') { // for display purposes
        checkout scm
    }
    container("python2") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Install Requirements') {
                sh "python -m pip install PyYaml dill pandas"
            }
            ws("${WORKSPACE}/src") {
                stage('Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
                stage('Integration Tests') {
                    sh "python -Wi -m unittest integration"
                }
                stage('Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/ssh_utils/") {
            stage('Install Requirements') {
                sh "python -m pip install pysftp"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/gcp_utils/") {
            stage('Install Requirements') {
                sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
    }
    container("python3") {
        ws("${WORKSPACE}/foundations_sdk/") {
            stage('Install Requirements') {
                sh "python -m pip install PyYaml dill pandas"
            }
            ws("${WORKSPACE}/src") {
                stage('Unit Tests') {
                    sh "python -Wi -m unittest test"
                }
                stage('Integration Tests') {
                    sh "python -Wi -m unittest integration"
                }
                stage('Acceptance Tests') {
                    sh "python -Wi -m unittest acceptance"
                }
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/ssh_utils/") {
            stage('Install Requirements') {
                sh "python -m pip install pysftp"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        ws("${WORKSPACE}/gcp_utils/") {
            stage('Install Requirements') {
                sh "python -m pip install google-api-python-client google-auth-httplib2 google-cloud-storage"
            }
            ws("${WORKSPACE}/src") {
            }
            stage('Create Artifact') {
                sh "python setup.py sdist bdist_wheel"
            }
        }
    }
    stage('Results') {
        archiveArtifacts artifacts: '**/*.whl', fingerprint: true
    }
}