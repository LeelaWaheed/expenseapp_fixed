pipeline {
    agent any

    environment {
        IMAGE_NAME = "expense-tracker-app"
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
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh '''
                    docker run --rm -v ${WORKSPACE}:/app -w /app $IMAGE_NAME bash -c "
                        echo 🔍 Verifying test folder...
                        ls -al /app/tests
                        echo 🧪 Running pytest...
                        pytest /app/tests --maxfail=1 --disable-warnings -v | tee /app/test-report.txt
                    "
                '''
            }
        }

        stage('Lint Code') {
            steps {
                echo '🔍 Running Pylint...'
                sh '''
                    docker run --rm -v ${WORKSPACE}:/app -w /app $IMAGE_NAME bash -c "
                        pip install pylint &&
                        pylint app | tee /app/pylint-report.txt
                    "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh '''
                    docker run --rm -v ${WORKSPACE}:/app -w /app $IMAGE_NAME bash -c "
                        pip install bandit &&
                        bandit -r app | tee /app/bandit-report.txt
                    "
                '''
            }
        }

        stage('Verify Reports') {
            steps {
                echo '📂 Verifying generated reports...'
                sh 'ls -al $WORKSPACE'
                sh 'cat $WORKSPACE/test-report.txt || echo ❌ test-report.txt not found'
                sh 'cat $WORKSPACE/pylint-report.txt || echo ❌ pylint-report.txt not found'
                sh 'cat $WORKSPACE/bandit-report.txt || echo ❌ bandit-report.txt not found'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying (stub)...'
                // Placeholder for real deployment step
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
