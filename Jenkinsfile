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
        sh 'docker tag expenseapp leelawaheed/expenseapp_fixed:latest' // Fix repository format
        sh 'docker push leelawaheed/expenseapp_fixed:latest'

        echo '🔄 Stopping existing container (if any)...'
        sh 'docker stop expenseapp || true'
        sh 'docker rm expenseapp || true'

        echo '🚀 Deploying new container...'
        sh 'docker run -d --name expenseapp -p 5000:5000 leelawaheed/expenseapp_fixed:latest'

        echo '🔍 Checking container logs for errors...'
        sh 'docker logs expenseapp'
    }
}
    }
}