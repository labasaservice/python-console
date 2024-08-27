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
                sh "python${env.PYTHON_VERSION} -m venv ${env.VENV_NAME}"
                sh ". ${env.VENV_NAME}/bin/activate"
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh ". ${env.VENV_NAME}/bin/activate && pytest tests"
            }
        }

        stage('Build') {
            steps {
                sh ". ${env.VENV_NAME}/bin/activate && python setup.py sdist bdist_wheel"
            }
        }

        stage('Upload to GitHub Artifacts') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                    RELEASE_ID=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                        "https://api.github.com/repos/${GITHUB_REPO}/releases/tags/${RELEASE_TAG}" | \
                        jq -r .id)
                    
                    if [ "$RELEASE_ID" = "null" ]; then
                        echo "Release not found. Creating a new release..."
                        RELEASE_ID=$(curl -s -X POST \
                            -H "Authorization: token $GITHUB_TOKEN" \
                            -H "Accept: application/vnd.github.v3+json" \
                            -d '{"tag_name":"'${RELEASE_TAG}'","name":"Release '${RELEASE_TAG}'","body":"Automated release '${RELEASE_TAG}'","draft":false,"prerelease":false}' \
                            "https://api.github.com/repos/${GITHUB_REPO}/releases" | \
                            jq -r .id)
                    fi

                    curl -X POST \
                    -H "Authorization: token $GITHUB_TOKEN" \
                    -H "Accept: application/vnd.github.v3+json" \
                    -H "Content-Type: application/zip" \
                    --data-binary @dist/${ARTIFACT_NAME} \
                    "https://uploads.github.com/repos/${GITHUB_REPO}/releases/${RELEASE_ID}/assets?name=${ARTIFACT_NAME}"
                    '''
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