pipeline {
    agent any

    stages {
        stage('Build api') {
            steps {
                dir('api') {
                    sh 'make build'
                }
            }
        }
        stage('Test api') {
            steps {
                dir('api') {
                    sh 'make test'
                }
            }
        }
        stage('Push api') {
            when {
                branch 'master'
            }
            steps {
                dir('api') {
                    sh 'make push'
                }
            }
        }
        stage('Build daemon') {
            steps {
                dir('daemon') {
                    sh 'make build'
                }
            }
        }
        stage('Test daemon') {
            steps {
                dir('daemon') {
                    sh 'make test'
                }
            }
        }
        stage('Push daemon') {
            when {
                branch 'master'
            }
            steps {
                dir('daemon') {
                    sh 'make push'
                }
            }
        }
        stage('Build gui') {
            steps {
                dir('gui') {
                    sh 'make build'
                }
            }
        }
        stage('Push gui') {
            when {
                branch 'master'
            }
            steps {
                dir('gui') {
                    sh 'make push'
                }
            }
        }
    }
}
