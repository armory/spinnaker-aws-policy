node {
    checkout scm
    stage("Build & Push") {
        sh('''
        export DOCKER_REGISTRY=docker.io/armory
        arm build
        arm push
        ''')
    }
}
