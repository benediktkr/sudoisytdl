pipeline {
    agent any
    stages {
        stage('build container') {
            steps {
                sh 'docker build -t benediktkr/sudoisytdl:latest .'
            }
        }

        stage('build package') {
            steps {
                sh 'docker run --name sudoisytdl_package benediktkr/sudoisytdl:latest build'
                sh 'mkdir -p dist'
                sh 'docker cp sudoisytdl_package:/ytdl/dist/* dist/'
            }
        }

        stage('docker publish') {
            steps {
                sh 'docker push benediktkr/sudoisytdl:latest'
            }
        }
    }

    post {
        always {
            sh 'docker rm sudoisytdl_package'
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            cleanWs()
        }
    }
}
