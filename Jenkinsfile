pipeline {
    agent any

    environment {
        IMAGE_NAME = 'expenseapp_fixed'
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
    echo '🧪 Running Pytest...'
    sh '''
        docker run --rm -v ${WORKSPACE}:/app -w /app expense-tracker-app bash -c "
            echo 🔍 Test folder content &&
            ls -al /app/tests &&
            pytest /app/tests --maxfail=1 --disable-warnings -v | tee /app/test-report.txt
        "
    '''
}


        stage('Lint Code') {
            steps {
                echo '🔍 Running Pylint...'
                sh "docker run --rm -v $WORKSPACE:/app -w /app $IMAGE_NAME bash -c 'pip install pylint && pylint app || true'"
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running Bandit...'
                sh "docker run --rm -v $WORKSPACE:/app -w /app $IMAGE_NAME bash -c 'pip install bandit && bandit -r app || true'"
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying (stub)...'
                // Add deployment logic here if needed
            }
        }
    }

    post {
        always {
            echo '📦 Build finished.'
        }
    }
}
