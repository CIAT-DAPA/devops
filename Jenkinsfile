/** Este código es un script de Jenkins Pipeline que implementa un proceso de despliegue (deployment) 
    automatizado para una API de Python en un servidor de AWS (Amazon Web Services) utilizando SSH.**/


def remote = [:] // Define an empty map for storing remote SSH connection parameters

pipeline {
    agent any // Se especifica que este pipeline puede ejecutarse en cualquier agente disponible

    environment {
        /** Se definen tres variables de entorno que se cargarán desde credenciales almacenadas en Jenkins.
            Estas variables son server_name, server_host y ssh_key. 
            Estas credenciales se utilizarán para establecer la conexión SSH con el servidor remoto.**/
        server_name = credentials('name_credencial')
        server_host = credentials('host_credencial')
        ssh_key = credentials('ssh_key_credential')
    }

    stages { //Se definen múltiples etapas que representan cada paso del proceso de implementación
        stage('Connection to AWS server') { 
            /** En esta etapa, se establece la conexión SSH con el servidor de AWS utilizando las credenciales proporcionadas.
                Se configuran los parámetros necesarios para la conexión SSH. **/
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                }
            }
        }

        stage('Verify Api folder and environment') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Verify and create the api_project folder if it does not exist and the virtual environment
                        if [ ! -d api_project ]; then
                            mkdir ./api_project
                            cd ./api_project
                            python3 -m venv env
                        fi
                    '''
                }
            }
        }
        
        stage('Stop previous API') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Stop the API if it is running
                        
                        cd ./api_project

                        if [ -f pid.txt ]; then
                            PID_API=$(cat pid.txt)
                            if kill -0 "$PID_API" 2>/dev/null; then
                                echo "The process exists, stopping it..."
                                kill "$PID_API"
                            fi
                        fi
                    '''
                }
            }
        }
        
        stage('Backup previous files') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Saving old API files
                        cd ./api_project
                        rm -rf api_previous
                        if [ -d api_current ]; then
                            mv api_current api_previous
                        fi
                    '''
                }
            }
        }
        
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Download the latest release from GitHub
                        cd ./api_project
                        rm -rf releaseApi.zip
                        curl -LOk https://github.com/user/repo/releases/latest/download/releaseApi.zip
                        rm -rf api_current
                        unzip releaseApi.zip -d api_current
                    '''
                }
            }
        }
        
        stage('Update dependencies') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        cd ./api_project
                        # Activate the virtual environment
                        source env/bin/activate

                        # Updating the dependencies
                        pip install --upgrade setuptools wheel
                        pip install -r api_current/requirements.txt
                    '''
                }
            }
        }
        
        stage('Start API') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Configure variables for deployment
                        while IFS= read -r line; do
                            export "$line"
                        done < variables.txt

                        # Activate the virtual environment
                        cd ./api_project
                        source env/bin/activate

                        # Start API
                        cd ./api_current
                        nohup python3 api.py > api.log 2>&1 &

                        # Get the new PID and save it to a file
                        PID_API=$!
                        echo $PID_API > ../pid.txt
                    '''
                }
            }
        }

        stage('Verify API') {
            // En esta etapa, se verifica si la API está funcionando correctamente haciendo una solicitud HTTP 
            // al servidor local (http://127.0.0.1:5000). Si la respuesta es 200, se muestra un mensaje de éxito; 
            // de lo contrario, se genera un error y se inicia una etapa de recuperación (post -> failure).**/
            steps {
                script {
                    def apiUrl = "http://127.0.0.1:5000"

                    def response = sshCommand remote: remote, command: "curl -sL -w \"%{http_code}\" -o /dev/null ${apiUrl}"

                    if (response.trim() == '200') {
                        echo "API is running correctly."
                    } else {
                        error "API is not running correctly. Rolling back..."
                    }
                }
            }
        }
    }

    post {
        // Estas etapas se ejecutan después de que se hayan completado todas las etapas anteriores, ya sea con éxito (success) o con un error (failure).
        failure { // En caso de un error (failure), se realiza una recuperación que restaura la versión anterior de la API.
            script {
                sshCommand remote: remote, command: '''
                    # Configure variables for deployment
                    while IFS= read -r line; do
                        export "$line"
                    done < variables.txt

                    # Rollback to the previous API if any step fails
                    cd ./api_SPCAT
                    rm -rf api_actual
                    mv api_antiguo api_actual

                    # Activate the virtual environment
                    source env/bin/activate

                    # Start API
                    cd ./api_actual
                    nohup python3 api.py > api_spcat.log 2>&1 &
                    
                    # Get the new PID and save it to a file
                    PID_API_SPCAT=$!
                    echo $PID_API_SPCAT > ../pid.txt
                '''
            }
        }

        success { // En caso de éxito (success), se muestra un mensaje de éxito
            script {
                echo 'everything went very well!!'
            }
        }
    }
}