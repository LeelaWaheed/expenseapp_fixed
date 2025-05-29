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

        stage('Test') {
    steps {
        echo '🧪 Running tests inside Docker container...'
        sh '''
            docker run --rm -v "$WORKSPACE:/app" -w /app expense-tracker-app bash -c "pytest > test-report.txt || true"
        '''
    }
}

stage('Code Quality') {
    steps {
        echo '🔍 Running pylint inside Docker...'
        sh '''
            docker run --rm -v "$WORKSPACE:/app" -w /app expense-tracker-app bash -c "pip install pylint && pylint app/ --exit-zero > pylint-report.txt"
        '''
    }
}

stage('Security Scan') {
    steps {
        echo '🔒 Running Bandit inside Docker...'
        sh '''
            docker run --rm -v "$WORKSPACE:/app" -w /app expense-tracker-app bash -c "pip install bandit && bandit -r app/ > bandit-report.txt || true"
        '''
    }
}


        stage('Deploy') {
            steps {
                echo '🚀 Deployment stage (stub)'
                // Add deployment steps here if needed
            }
        }
    }

    post {
        always {
            echo '📦 Archiving reports...'
            archiveArtifacts artifacts: '**.txt', allowEmptyArchive: true
        }
    }
}
