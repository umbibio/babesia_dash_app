#!/bin/sh

if [ ! -f .initialized ]; then                                                                                                                                                                                    
    echo "Initializing container"                                                                                                                                                                                 
    # run initializing commands                                                                                                                                                                                   
    pip install --upgrade pip
    pip install dash dash-bootstrap-components dash-bootstrap-templates dash-cytoscape pandas mysql-connector-python gunicorn
    touch .initialized                                                                                                                                                                                            
fi 

exec "$@"
