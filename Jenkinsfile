pipeline {
    agent any

    environment {
        IMAGE_NAME = 'expense-tracker-app'
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

        stage('Debug Workspace') {
            steps {
                echo '📂 Listing Jenkins workspace contents before Docker runs...'
                sh 'ls -al $WORKSPACE'
            }
        }

    stage('Test') {
        steps {
            echo '🧪 Verifying requirements.txt inside container...'
            sh """
                docker run --rm -v "$WORKSPACE:/app" -w /app python:3.11 bash -c "ls -al /app && cat requirements.txt || echo '❌ requirements.txt still not found!'"
            """
        }
    }


        stage('Code Quality') {
            steps {
                echo '🔍 Running pylint inside Docker...'
                sh '''
                    docker run --rm -v "$WORKSPACE:/app" -w /app python:3.11 bash -c '
                        pip install -r requirements.txt &&
                        pip install pylint &&
                        pylint app/ --exit-zero > pylint-report.txt
                    '
                '''
            }
        }

        stage('Security Scan') {
            when {
                expression { fileExists('app/') }
            }
            steps {
                echo '🛡️ Security scanning... (placeholder)'
                // Add Bandit or other scanners here
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying container... (placeholder)'
                // Add actual deploy commands here
            }
        }
    }

    post {
        always {
            echo '📦 Archiving reports...'
            archiveArtifacts artifacts: '**/*.txt', allowEmptyArchive: true
        }
    }
}
