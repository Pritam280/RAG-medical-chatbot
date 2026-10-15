// pipeline {
//     agent any

//     environment {
//         AWS_REGION = 'us-east-1'
//         ECR_REPO = 'myrepo'
//         IMAGE_TAG = 'latest'
//         SERVICE_NAME = 'llmops-medical-service'
//     }

//     stages {
//         stage('Clone GitHub Repo') {
//             steps {
//                 script {
//                     echo 'Cloning GitHub repo to Jenkins...'
//                     checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Pritam280', url: 'https://github.com/Pritam280/RAG-medical-chatbot.git']])
//                 }
//             }
//         }

//         stage('Build, Scan, and Push Docker Image to ECR') {
//             steps {
//                 withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
//                     script {
//                         def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
//                         def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
//                         def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

//                         sh """
//                         aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
//                         docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
//                         trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true
//                         docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
//                         docker push ${imageFullTag}
//                         """

//                         archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
//                     }
//                 }
//             }
//         }

//         //  stage('Deploy to AWS App Runner') {
//         //     steps {
//         //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
//         //             script {
//         //                 def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
//         //                 def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
//         //                 def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

//         //                 echo "Triggering deployment to AWS App Runner..."

//         //                 sh """
//         //                 SERVICE_ARN=\$(aws apprunner list-services --query "ServiceSummaryList[?ServiceName=='${SERVICE_NAME}'].ServiceArn" --output text --region ${AWS_REGION})
//         //                 echo "Found App Runner Service ARN: \$SERVICE_ARN"

//         //                 aws apprunner start-deployment --service-arn \$SERVICE_ARN --region ${AWS_REGION}
//         //                 """
//         //             }
//         //         }
//         //     }
//         // }
//     }
// }





pipeline {
    agent any

    environment {
        AWS_REGION   = 'us-east-1'
        ECR_REPO     = 'myrepo'   // must match a real ECR repo name
        IMAGE_TAG    = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Pritam280', url: 'https://github.com/Pritam280/RAG-medical-chatbot.git']])
                }
            }
        }

        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId    = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrRegistry  = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                        def ecrUrl       = "${ecrRegistry}/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${env.IMAGE_TAG}"

                        echo "Registry = ${ecrRegistry}"

                        sh """
                        aws ecr get-login-password --region ${env.AWS_REGION} | docker login --username AWS --password-stdin ${ecrRegistry}
                        docker build -t ${env.ECR_REPO}:${env.IMAGE_TAG} .
                        """

                        // Trivy via container (uses the mounted docker socket, nothing to install)
                        sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image \
                          --severity HIGH,CRITICAL --format json \
                          ${env.ECR_REPO}:${env.IMAGE_TAG} > trivy-report.json || true
                        """

                        sh """
                        docker tag ${env.ECR_REPO}:${env.IMAGE_TAG} ${imageFullTag}
                        docker push ${imageFullTag}
                        """

                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }
    }
}