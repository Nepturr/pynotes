pipeline {
    agent none
    stages {
        stage("Build & Analyse avec SonarQube") { 
            agent any
            steps { 
                script {
                    sh 'mvn clean package sonar:sonar'
                }
            }
        }
        stage("Deploy & OWASP Dependency-Check") {
            agent any
            steps {
                dependencyCheck additionalArguments: '''
                    -o './'
                    -s './'
                    -f 'ALL'
                    --prettyPrint''', 
                    odcInstallation: 'Dependency-Check'
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
    }
}
