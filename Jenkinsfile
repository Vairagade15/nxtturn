pipeline {
    agent any

    environment {
        APP_NAME = "nxtturn"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
            }
        }

        /* =======================
           TESTING BRANCH PIPELINE
           ======================= */
        stage('Verify Test Files') {
            when {
                branch 'testing'
            }
            steps {
                sh '''
                echo "Workspace:"
                pwd
                echo "Listing files:"
                ls -la
                echo "Checking docker-compose.test.yml"
                test -f docker-compose.test.yml
                '''
            }
        }

        stage('Build Backend Image (Testing)') {
            when {
                branch 'testing'
            }
            steps {
                sh '''
                docker build -t nxtturn:test ./Loopline
                '''
            }
        }

        stage('Run Django Tests (Docker)') {
            when {
                branch 'testing'
            }
            steps {
                sh '''
                echo "Creating test environment file"

                cat <<EOF > .env.test
DJANGO_SETTINGS_MODULE=config.settings
DATABASE_URL=postgres://test:test@db:5432/test_db
DEBUG=False
EOF

                echo "Running test containers"
                docker-compose -f docker-compose.test.yml up \
                  --build \
                  --abort-on-container-exit \
                  --exit-code-from backend-test
                '''
            }
        }

        /* =======================
           MAIN BRANCH PIPELINE
           ======================= */
        stage('Build Production') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                echo "Running production build for main branch"
                docker-compose build
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker-compose -f docker-compose.test.yml down -v || true
            docker system prune -f || true
            '''
        }
        success {
            echo '✅ Pipeline PASSED'
        }
        failure {
            echo '❌ Pipeline FAILED'
        }
    }
}

