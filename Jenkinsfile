pipeline {
    agent any

    environment {
        DOCKER_REPO = 'https://github.com/LeelaWaheed/expenseapp_fixed'
        IMAGE_VERSION = '1.1' 
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
                echo 'Running tests inside Docker with coverage...'
                sh '''
                    docker run --rm \
                    -v "$(pwd)/coverage:/app/coverage" \
                    -w /app \
                    expenseapp \
                    sh -c "pytest --cov=app --cov-report=xml:coverage/coverage.xml tests/"
                '''
            }
        }

        stage('Lint Code') {
            steps {
                echo 'Running Pylint...'
                sh '''
                    docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    expenseapp \
                    sh -c "
                        pip install pylint &&
                        pylint app --output-format=text | tee pylint-report.txt || true
                    "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Bandit...'
                sh '''
                    docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    expenseapp \
                    sh -c "
                        pip install bandit &&
                        bandit -r app -f txt | tee bandit-report.txt || true
                    "
                '''
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                echo 'Running SonarCloud Analysis...'
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm \
                        -v "$(pwd)":/usr/src \
                        -w /usr/src \
                        sonarsource/sonar-scanner-cli \
                        sonar-scanner \
                        -Dsonar.projectKey=expenseapp_fixed \
                        -Dsonar.organization=leelawaheed \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=https://sonarcloud.io \
                        -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        /* 
        stage('Deploy') {
            steps {
                echo "Tagging and pushing Docker image as ${DOCKER_REPO}:${IMAGE_VERSION}"
        
                sh "docker tag expenseapp ${DOCKER_REPO}:${IMAGE_VERSION}"

                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
                sh "docker push ${DOCKER_REPO}:${IMAGE_VERSION}"
            }
        }
    }
     */
}
