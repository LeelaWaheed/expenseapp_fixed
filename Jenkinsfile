pipeline {
    agent any
    
    environment {
        DOCKER_REPO = 'myrepo/expenseapp'  // Replace with your actual Docker repository
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'docker build -t expenseapp .'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest'  // Ensure you have pytest installed
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Analyzing code quality...'
                sh 'pylint --disable=all --enable=unused-import,wrong-import-position $(git ls-files "*.py")'
            }
        }
        
        stage('Security') {
            steps {
                echo 'Running security scans...'
                sh 'bandit -r .'  // Bandit for Python security checks
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                
                echo 'Tagging and pushing Docker image...'
                sh 'docker tag expenseapp $DOCKER_REPO:latest'
                sh 'docker push $DOCKER_REPO:latest'  // Push to your Docker repository
                
                echo 'Stopping old container (if exists)...'
                sh 'docker stop expenseapp || true'
                sh 'docker rm expenseapp || true'
                
                echo 'Running new container...'
                sh 'docker run -d --name expenseapp -p 5000:5000 $DOCKER_REPO:latest'
            }
        }
    }
}