pipeline {
    agent any

    environment {
        GITHUB_REPO = 'labasaservice/python-console'
        RELEASE_TAG = 'v0.1.0'
        ARTIFACT_NAME = 'word-counter-0.1.0.tar.gz'
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
    }

 stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    def pythonCmd = sh(script: 'which python3', returnStdout: true).trim()
                    if (!pythonCmd) {
                        error "Python 3 not found. Please install Python 3 on the Jenkins server."
                    }
                    sh "echo Using Python: \$(${pythonCmd} --version)"
                    sh "${pythonCmd} -m venv ${env.VENV_NAME}"
                    sh ". ${env.VENV_NAME}/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
                }
            }
        }

        stage('Test') {
            steps {
                sh ". ${env.VENV_NAME}/bin/activate && python -m pytest tests"
            }
        }

        stage('Build') {
            steps {
                sh ". ${env.VENV_NAME}/bin/activate && python setup.py sdist bdist_wheel"
            }
        }

        stage('Upload to GitHub Artifacts') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                        def releaseId = sh(script: """
                            curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
                            "https://api.github.com/repos/${GITHUB_REPO}/releases/tags/${RELEASE_TAG}" | \
                            jq -r .id
                        """, returnStdout: true).trim()

                        if (releaseId == "null") {
                            echo "Release not found. Creating a new release..."
                            releaseId = sh(script: """
                                curl -s -X POST \
                                -H "Authorization: token ${GITHUB_TOKEN}" \
                                -H "Accept: application/vnd.github.v3+json" \
                                -d '{"tag_name":"${RELEASE_TAG}","name":"Release ${RELEASE_TAG}","body":"Automated release ${RELEASE_TAG}","draft":false,"prerelease":false}' \
                                "https://api.github.com/repos/${GITHUB_REPO}/releases" | \
                                jq -r .id
                            """, returnStdout: true).trim()
                        }

                        sh """
                            curl -X POST \
                            -H "Authorization: token ${GITHUB_TOKEN}" \
                            -H "Accept: application/vnd.github.v3+json" \
                            -H "Content-Type: application/zip" \
                            --data-binary @dist/${ARTIFACT_NAME} \
                            "https://uploads.github.com/repos/${GITHUB_REPO}/releases/${releaseId}/assets?name=${ARTIFACT_NAME}"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}