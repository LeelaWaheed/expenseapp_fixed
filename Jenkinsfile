pipeline {
    agent any

    environment {
        DOCKER_REPO = 'https://github.com/LeelaWaheed/expenseapp_fixed' // Replace with your actual Docker repository
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t expenseapp .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests inside Docker...'
                sh 'docker run --rm expenseapp pytest' // Runs tests within a clean container
            }
        }

stage('Lint Code') {
    steps {
        echo '🔍 Running Pylint...'
        sh '''
            docker run --rm -v "expenseapp:/app" -w /app expenseapp sh -c "
                pip install pylint &&
                pylint app --output-format=text | tee pylint-report.txt || true
            "
        '''
        
    }
}

stage('Security Scan') {
    steps {
        echo '🔒 Running Bandit...'
        sh '''
            docker run --rm -v "expenseapp:/app" -w /app expenseapp sh -c "
                pip install bandit &&
                bandit -r app -f txt | tee bandit-report.txt || true
            "
        '''
        
    }
}



 stage('Deploy') {
    steps {
        echo '🚀 Tagging and pushing Docker image...'
        sh 'docker tag expenseapp leela/expenseapp_fixed:latest'
        
        // Secure Docker login using Jenkins credentials
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
        }

        sh 'docker push leela/expenseapp_fixed:latest'
    }
}
    }
}