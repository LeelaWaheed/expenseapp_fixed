pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/LeelaWaheed/expense-track-app'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t expense-tracker-app .'
            }
        }

    stage('Run Tests') {
    steps {
        echo '🧪 Running Pytest...'
        sh '''
            docker run --rm -v ${WORKSPACE}:/app -w /app expense-tracker-app bash -c "
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
                    docker run --rm -v $(pwd):/app -w /app expense-tracker-app bash -c "
                        pip install pylint
                        pylint app > pylint-report.txt || true
                    "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh '''
                    docker run --rm -v $(pwd):/app -w /app expense-tracker-app bash -c "
                        pip install bandit
                        bandit -r app > bandit-report.txt || true
                    "
                '''
            }
        }

        stage('Verify Reports') {
            steps {
                echo '📂 Verifying generated reports...'
                sh 'ls -al'
                sh 'cat test-report.txt || echo "❌ test-report.txt not found"'
                sh 'cat pylint-report.txt || echo "❌ pylint-report.txt not found"'
                sh 'cat bandit-report.txt || echo "❌ bandit-report.txt not found"'
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
