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
                sh '''
                    docker build --no-cache -t expense-tracker-app .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh '''
                    docker run --rm -v $(pwd):/app -w /app expense-tracker-app bash -c "
                        echo 📂 Verifying tests directory:
                        ls -R /app/tests || echo '❌ /app/tests not found'

                        echo 🔍 Checking Python:
                        which python && python --version

                        echo 🧪 Running pytest:
                        pytest tests --maxfail=1 --disable-warnings -v | tee test-report.txt
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
                        pylint app > pylint-report.txt || echo '❌ Pylint failed'
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
                        bandit -r app > bandit-report.txt || echo '❌ Bandit failed'
                    "
                '''
            }
        }

        stage('Verify Reports') {
            steps {
                echo '📂 Verifying generated reports...'
                sh '''
                    echo 📄 Contents of test-report.txt:
                    cat test-report.txt || echo '❌ test-report.txt not found'

                    echo 📄 Contents of pylint-report.txt:
                    cat pylint-report.txt || echo '❌ pylint-report.txt not found'

                    echo 📄 Contents of bandit-report.txt:
                    cat bandit-report.txt || echo '❌ bandit-report.txt not found'
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
