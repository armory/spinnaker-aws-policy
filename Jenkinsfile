node {
    checkout scm
    stage("Build & Test") {
      sh('''
        ./bin/build
        ./bin/test
      ''')
    }
    stage("Push") {
      sh('''
        ./bin/push
      ''')
    }
}
