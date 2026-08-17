pipeline {
    agent any

    stages {

        stage('Fetch Images') {
            steps {
                script {

                    def imageTags = sh(
                        script: '/opt/jenkins-python/bin/python get_images.py',
                        returnStdout: true
                    ).trim()

                    echo "Images found:"
                    echo imageTags

                    env.IMAGE_TAGS = imageTags
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