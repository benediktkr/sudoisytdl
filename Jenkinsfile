pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'docker build -t benediktkr/sudoisytdl:latest .'
                sh 'docker run --rm benediktkr/sudoisytdl:latest build'
            }
        }

        stage('publish') {
            steps {
                sh 'docker push benediktkr/sudoisytdl:latest'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
        }
    }
}
