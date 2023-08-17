pipeline {

    agent any

    environment {

        DOCKER_REGISTRY = "raguyazhin"
        DOCKER_IMAGE_NAME = "ping-poller-api"
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}.0.0"


        APP_GIT_REPO_URL = "https://github.com/raguyazhin/ping-poller-app.git"
        APP_GIT_REPO_BRANCH = "master"

        KUBE_MANIFEST_GIT_REPO_URL = "https://github.com/raguyazhin/ping-poller-manifest.git"
        KUBE_MANIFEST_GIT_REPO_BRANCH = "master"
        KUBE_MANIFEST_FILE = "ping-poller-deploy.yaml"

        KUBECONFIG = "C:\\\\Users\\\\3100002\\\\.kube\\\\config"

    }

    stages {

        stage('Clone App repository') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "${APP_GIT_REPO_BRANCH}"]],
                    userRemoteConfigs: [[url: "${APP_GIT_REPO_URL}"]],
                    extensions: [[$class: 'CloneOption', depth: 1, shallow: true]]
                ])    
            }
        }     
           
        stage('Build Docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ragudockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    script {
                        def workspacePath = env.WORKSPACE.replace(File.separator, "\\\\")
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${workspacePath}"
                    }
                }
            }
        }
    
        // stage('Push Docker image') {

        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'ragudockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
        //             sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
        //             sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
        //         }                
        //     }
        // }


        // stage('Clone Kube Manifest repository') {
        //     steps {
        //         checkout([
        //             $class: 'GitSCM',
        //             branches: [[name: "${KUBE_MANIFEST_GIT_REPO_BRANCH}"]],
        //             userRemoteConfigs: [[url: "${KUBE_MANIFEST_GIT_REPO_URL}"]],
        //             extensions: [[$class: 'CloneOption', depth: 1, shallow: true]]
        //         ])    
        //     }
        // }

        // stage('switch to master branch') {
        //     steps {
        //         sh "git checkout master"
        //     }
        // }

        // stage('Update image in kube manifest in local jenkins workspace') {
        //     steps {
        //        script {

        //             // def workspacePath = env.WORKSPACE.replace(File.separator, "\\\\")
        //             // def yaml = readYaml(file: "${workspacePath}\\\\${KUBE_MANIFEST_FILE}")
        //             // sh "echo ${yaml}"
        //             // yaml.spec.template.spec.containers[0].image = "${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
        //             // writeYaml(file: "${workspacePath}\\\\${KUBE_MANIFEST_FILE}", data: yaml, overwrite: true )
                   
        //             def yaml = readYaml(file: "${KUBE_MANIFEST_FILE}")
        //             yaml.spec.template.spec.containers[0].image = "${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
        //             writeYaml(file: "${KUBE_MANIFEST_FILE}", data: yaml, overwrite: true )

        //         }
        //     }
        // }   

        // stage('Commit and push changes to kube manifest GitHub Repository') {
        //     steps {                                
        //         withCredentials([string(credentialsId: 'ragugithubtoken', variable: 'GIT_TOKEN')]) {

        //             sh """    
        //                 git config user.email 'raguyazhin@gmail.com'
        //                 git config user.name 'Ragu Thangavel'            
        //                 git add .
        //                 git commit -m 'Update image (${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}) in Kube manifest' 
        //                 git push https://${GIT_TOKEN}@github.com/raguyazhin/ping-poller-manifest.git                                                    
        //             """
        //         }
        //     }
        // }

        // stage('Deploy to Kubernetes') {
        //     steps {
        //         sh "kubectl apply -f ping-poller-deploy.yaml"
        //         sh "kubectl apply -f ping-poller-svc.yaml"
        //     }
        // }

    }
}