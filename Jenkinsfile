
pipeline {
  agent {
    // Image with Python & Chrome installed; replace with your org-approved image if needed.
    docker { image 'ghcr.io/ultrafunkamsterdam/python3.11-chrome:latest' }
  }

  // Daily schedule around 07:00 (server time, hashed by job name)
  triggers { cron('H 7 * * *') }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Install deps') {
      steps {
        sh '''
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run screenshots') {
      steps {
        sh 'python screenshot_selenium.py'
      }
    }

    stage('Archive screenshots') {
      steps {
        archiveArtifacts artifacts: 'screenshots/*.png', fingerprint: true
      }
    }
  }

  post {
    success { echo "Full-page screenshot job succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
    failure { echo "Full-page screenshot job failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
  }
}
