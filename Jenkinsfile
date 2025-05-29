pipeline {
    agent any

    environment {
        IMAGE_NAME = 'expense-tracker-app'
        WORKDIR = '/app'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh """
                    docker run --rm -v \$PWD:${WORKDIR} -w ${WORKDIR} $IMAGE_NAME \
                    bash -c "pytest tests > test-report.txt || true"
                """
            }
        }

        stage('Lint Code') {
            steps {
                echo '🔍 Running Pylint...'
                sh """
                    docker run --rm -v \$PWD:${WORKDIR} -w ${WORKDIR} $IMAGE_NAME \
                    bash -c "pip install pylint && pylint app > pylint-report.txt || true"
                """
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh """
                    docker run --rm -v \$PWD:${WORKDIR} -w ${WORKDIR} $IMAGE_NAME \
                    bash -c "pip install bandit && bandit -r app > bandit-report.txt || true"
                """
            }
        }

        stage('Verify Reports') {
            steps {
                echo '📂 Verifying generated reports...'
                sh '''
                    ls -al
                    cat test-report.txt || echo "❌ test-report.txt not found"
                    cat pylint-report.txt || echo "❌ pylint-report.txt not found"
                    cat bandit-report.txt || echo "❌ bandit-report.txt not found"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying (stub)...'
            }
        }
    }

    post {
        always {
            echo '📦 Archiving reports...'
            archiveArtifacts artifacts: '*.txt', allowEmptyArchive: true
        }
    }
}
