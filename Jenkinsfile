pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'expense-tracker-app'
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
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh '''
                    docker run --rm -v "$WORKSPACE:/app" -w /app $DOCKER_IMAGE bash -c "pytest tests > /app/test-report.txt || true"
                '''
            }
        }

        stage('Lint Code') {
            steps {
                echo '🔍 Running Pylint...'
                sh '''
                    docker run --rm -v "$WORKSPACE:/app" -w /app $DOCKER_IMAGE bash -c "pip install pylint && pylint app > /app/pylint-report.txt || true"
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh '''
                    docker run --rm -v "$WORKSPACE:/app" -w /app $DOCKER_IMAGE bash -c "pip install bandit && bandit -r app > /app/bandit-report.txt || true"
                '''
            }
        }

        stage('Verify Reports') {
            steps {
                echo '📂 Verifying generated reports...'
                sh 'ls -al $WORKSPACE'
                sh 'cat $WORKSPACE/test-report.txt || echo "❌ test-report.txt not found"'
                sh 'cat $WORKSPACE/pylint-report.txt || echo "❌ pylint-report.txt not found"'
                sh 'cat $WORKSPACE/bandit-report.txt || echo "❌ bandit-report.txt not found"'
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
