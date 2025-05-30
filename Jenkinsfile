pipeline {
    agent any

 stages {
        stage('Checkout') {
            steps {
                echo '📥 Cloning Repository...'
                checkout scm
            }
        }
stage('Build & Start Services') {
    steps {
        echo '🐳 Building and starting Flask app...'
        sh '''
            docker-compose up -d --build
        '''
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
                pylint app | tee /app/pylint-report.txt || true
            "
        '''
    }
}

stage('Security Scan') {
    steps {
        echo '🔒 Running Bandit...'
        sh '''
            docker run --rm -v "/var/jenkins_home/workspace/hdtask:/workspace" -w /workspace expense-tracker-app bash -c "
                mkdir -p /app &&
                cp -r /workspace/* /app/ &&
                ls -al /app &&
                find /app -name '*.py' &&
                pip install --quiet bandit &&
                bandit /app/**/*.py --verbose || true
            "
        '''
    }
}


stage('Verify Reports') {
    steps {
        echo '📂 Verifying generated reports...'
        sh '''
            ls -al
            [ -f test-report.txt ] && cat test-report.txt || echo "❌ test-report.txt not found"
            [ -f pylint-report.txt ] && cat pylint-report.txt || echo "❌ pylint-report.txt not found"
            [ -f bandit-report.txt ] && cat bandit-report.txt || echo "❌ bandit-report.txt not found"
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