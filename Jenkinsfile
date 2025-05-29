pipeline {
  agent any

  environment {
    COVERAGE_DIR = "htmlcov"
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
        sh 'docker build -t expense-tracker-app .'
      }
    }

    stage('Test') {
      steps {
        echo '🧪 Installing dependencies and running tests inside Docker...'
        sh '''
          docker run --rm -v $PWD:/app -w /app python:3.11 bash -c "
            pip install -r requirements.txt &&
            pip install pytest pytest-cov &&
            pytest --cov=app --cov-report=term --cov-report=html:htmlcov > coverage-report.txt
          "
        '''
      }
    }

    stage('Code Quality') {
      steps {
        echo '🔍 Running pylint inside Docker...'
        sh '''
          docker run --rm -v $PWD:/app -w /app python:3.11 bash -c "
            pip install pylint &&
            pylint app/ --exit-zero > pylint-report.txt
          "
        '''
      }
    }

    stage('Security Scan') {
      steps {
        echo '🔐 Running Bandit inside Docker...'
        sh '''
          docker run --rm -v $PWD:/app -w /app python:3.11 bash -c "
            pip install bandit &&
            bandit -r app/ > bandit-report.txt
          "
        '''
      }
    }

    stage('Deploy') {
      steps {
        echo '🚀 Deploying Docker container...'
        sh '''
          docker rm -f expense-tracker || true
          docker run -d -p 5000:5000 --name expense-tracker expense-tracker-app
        '''
      }
    }
  }

  post {
    always {
      echo '📦 Archiving reports...'
      archiveArtifacts artifacts: 'coverage-report.txt'
      archiveArtifacts artifacts: 'htmlcov/**'
      archiveArtifacts artifacts: 'pylint-report.txt'
      archiveArtifacts artifacts: 'bandit-report.txt'
    }
  }
}
