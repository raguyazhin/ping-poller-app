pipeline {

    agent any

    environment {

        DOCKER_REGISTRY = "raguyazhin"
        DOCKER_IMAGE_NAME = "node-backend-app"
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}.0.0"

        APP_GIT_REPO_URL = "https://github.com/raguyazhin/node-backend-app.git"
        APP_GIT_REPO_BRANCH = "master"

        KUBE_MANIFEST_GIT_REPO_URL = "https://github.com/raguyazhin/kube-manifest-node-backend-app.git"
        KUBE_MANIFEST_GIT_REPO_BRANCH = "master"
        KUBE_MANIFEST_FILE = "node-backend-deployment.yaml"

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
                script {
                    def workspacePath = env.WORKSPACE.replace(File.separator, "\\\\")
                    sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${workspacePath}"
                }
            }
        }

        stage('Push Docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ragudockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {                
                    sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                }
            }
        }

        stage('Clone Kube Manifest repository') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master' ]],
                    userRemoteConfigs: [[credentialsId: 'ragudockerhub', url: "${KUBE_MANIFEST_GIT_REPO_URL}"]],
                    extensions: [[$class: 'CloneOption', depth: 1, shallow: true]]
                ])
            }
        }  

        stage('switch to master branch') {
            steps {
                sh "git checkout master"
            }
        }

        // Plugin - Pipeline Utility Steps
        stage('Update image in kube manifest in local jenkins workspace') {
            steps {
               script {

                    // def workspacePath = env.WORKSPACE.replace(File.separator, "\\\\")
                    // def yaml = readYaml(file: "${workspacePath}\\\\${KUBE_MANIFEST_FILE}")
                    // sh "echo ${yaml}"
                    // yaml.spec.template.spec.containers[0].image = "${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    // writeYaml(file: "${workspacePath}\\\\${KUBE_MANIFEST_FILE}", data: yaml, overwrite: true )
                   
                    def yaml = readYaml(file: "${KUBE_MANIFEST_FILE}")
                    yaml.spec.template.spec.containers[0].image = "${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    writeYaml(file: "${KUBE_MANIFEST_FILE}", data: yaml, overwrite: true )

                }
            }
        }   

        stage('Commit and push changes to kube manifest GitHub Repository') {
            steps {                                
                withCredentials([string(credentialsId: 'ragudockerhubtoken', variable: 'GIT_TOKEN')]) {

                    // git config user.email 'jenkins@example.com'
                    // git config user.name 'Jenkins'
                    //git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${KUBE_MANIFEST_GIT_REPO_URL} ${KUBE_MANIFEST_GIT_REPO_BRANCH}
                    //git push origin HEAD:master
                    //git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/raguyazhin/kube-manifest-node-backend-app.git HEAD:master
                    //git push ${KUBE_MANIFEST_GIT_REPO_URL} HEAD:${KUBE_MANIFEST_GIT_REPO_BRANCH} -u ${GIT_TOKEN}
                    //git push -u ${KUBE_MANIFEST_GIT_REPO_URL} HEAD:${KUBE_MANIFEST_GIT_REPO_BRANCH} ${GIT_TOKEN}

                    sh """    
                        git config user.email 'raguyazhin@gmail.com'
                        git config user.name 'Ragu Thangavel'            
                        git add .
                        git commit -m 'Update image (${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}) in Kube manifest' 
                        git push https://${GIT_TOKEN}@github.com/raguyazhin/kube-manifest-node-backend-app.git                                                    
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f node-backend-deployment.yaml"
                sh "kubectl apply -f node-backend-clusterip-svc.yaml"
            }
        }

    }
}