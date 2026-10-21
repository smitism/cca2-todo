
pipeline {
    agent { label 'windows-docker' }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE = 'smit172006/cca2-todo'
        DOCKER_CREDS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/smitism/cca2-todo.git'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m unittest discover -s tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE%:%BUILD_NUMBER% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    powershell '''
                        $env:DOCKER_TOKEN | docker login -u $env:DOCKER_USER --password-stdin
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                        docker push "$($env:IMAGE):$($env:BUILD_NUMBER)"
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/'
                bat 'kubectl set image deployment/cca2-todo cca2-todo=%IMAGE%:%BUILD_NUMBER%'
                bat 'kubectl rollout status deployment/cca2-todo --timeout=180s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get pods'
                bat 'kubectl get services'
                bat 'kubectl get deployment cca2-todo'
            }
        }
    }

    post {
        success {
            echo 'CCA2 CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage in Console Output.'
        }
    }
}
