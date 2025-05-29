pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/LeelaWaheed/expenseapp_fixed'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build --no-cache -t expense-tracker-app .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh '''
                    docker run --rm expense-tracker-app bash -c "
                        ls -al /app/tests || echo '❌ tests folder not found'
                        pytest tests --maxfail=1 --disable-warnings -v | tee test-report.txt
                    "
                '''
            }
        }

        stage('Lint Code') {
            steps {
                echo '🔍 Running Pylint...'
                sh '''
                    docker run --rm expense-tracker-app bash -c "
                        pip install --quiet pylint &&
                        echo '🔍 Linting files...' &&
                        pylint app | tee pylint-report.txt
                    "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh '''
                    docker run --rm expense-tracker-app bash -c "
                        pip install --quiet bandit &&
                        bandit -r app -f txt -o bandit-report.txt
                    "
                '''
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