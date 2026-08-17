pipeline {
    agent any

    stages {

//        stage('Fetch Images') {
//            steps {
//                script {
//
//                    def imageTags = sh(
//                        script: '/opt/jenkins-python/bin/python get_images.py',
//                        returnStdout: true
//                    ).trim()
//
//                    echo "Images found:"
//                    echo imageTags
//
//                    env.IMAGE_TAGS = imageTags
//                }
//            }
//        }

        stage('Fetch Images') {
            steps {
                withCredentials([
                    string(credentialsId: 'jenkins_aws_access_key_id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'jenkins_aws_secret_access_key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    script {
                        def imageTags = sh(
                            script: '/opt/jenkins-python/bin/python get_images.py',
                            returnStdout: true
                        ).trim()

                        echo imageTags
                        env.IMAGE_TAGS = imageTags
                    }
                }
            }
        }

        stage('Select Image') {
            steps {
                script {

                    def selectedImage = input(
                        message: 'Select image to deploy',
                        parameters: [
                            choice(
                                name: 'IMAGE_TAG',
                                choices: env.IMAGE_TAGS,
                                description: 'Select image from ECR'
                            )
                        ]
                    )

                    echo "Selected image: ${selectedImage}"

                    env.SELECTED_IMAGE = selectedImage
                }
            }
        }
    }
}