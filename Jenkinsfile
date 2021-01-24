pipeline {
    agent any
    options {
        timestamps()
        ansiColor("xterm")
    }
    environment {
        NAME="${JOB_NAME.split('/')[1]}"
    }
    stages {
        stage('build container') {
            steps {
                sh "docker build -t benediktkr/${NAME}:latest ."
            }
        }

        stage('build package') {
            steps {
                sh "docker run --name ${NAME}_jenkins benediktkr/${NAME}:latest build"
                sh "docker cp ${NAME}_jenkins:/sudois/dist ."
            }
        }

        stage('docker publish latest') {
            when { not { tag "v*" } }
            steps {
                sh "docker push benediktkr/${NAME}:latest"
            }
        }

        stage('docker publish version') {
            when { tag "v*" }
            steps {
                sh "docker tag benediktkr/${NAME}:latest benediktkr/${NAME}:${TAG_NAME}"
                sh "docker push benediktkr/${NAME}:${TAG_NAME}"
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/*.tar.gz,dist/*.whl', fingerprint: true
        }
        cleanup {
            sh "docker rm ${NAME}_jenkins"
            cleanWs(deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
