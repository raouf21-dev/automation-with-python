pipeline {
    agent any

    stages {

        stage('Select Image') {
            steps {
                script {

                    def selectedImage = input(
                        message: 'Select image to deploy',
                        parameters: [
                            choice(
                                name: 'IMAGE_TAG',
                                choices: ['1.0', '2.0', '3.0'],
                                description: 'Choose Docker image version'
                            )
                        ]
                    )
                    echo "You selected: ${selectedImage}"
                }
            }
        }
    }
}