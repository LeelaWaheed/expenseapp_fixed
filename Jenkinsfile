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
        sh 'cat pylint-report.txt' // Displays the linting report in Jenkins console
    }
}

stage('Security Scan') {
    steps {
        echo '🔒 Running Bandit...'
        sh '''
            docker run --rm -v "expenseapp:/app" -w /app expenseapp sh -c "
                pip install bandit &&
                bandit -r app --severity-level low --confidence-level low -f txt -o bandit-report.txt || true
            "
        '''
        sh 'cat bandit-report.txt' // Displays the report in Jenkins console
    }
}



        stage('Deploy') {
            steps {
                echo 'Tagging and pushing Docker image to repository...'
                sh 'docker tag expenseapp $DOCKER_REPO:latest'
                sh 'docker push $DOCKER_REPO:latest'

                echo 'Stopping existing container (if any)...'
                sh 'docker stop expenseapp || true'
                sh 'docker rm expenseapp || true'

                echo 'Deploying new container...'
                sh 'docker run -d --name expenseapp -p 5000:5000 $DOCKER_REPO:latest'

                echo 'Checking container logs for errors...'
                sh 'docker logs expenseapp'
            }
        }
    }
}