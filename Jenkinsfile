pipeline {
    stages {
        stage('build') {
            steps {
                sh 'docker build -t benediktkr/sudoisytdl:latest .'
            }
        }

        stage('publish') {
            steps {
                sh 'docker push benediktkr/sudoisytdl:latest'
            }
        }
    }
}
