#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

#####################################
FISSION_NAMESPACE=default

ENV_NAME="python"

PKG_NAME="helloworld"

FN_NAME="helloworld"
FN_ENTRYPOINT="helloworld.main"

ROUTE_NAME="helloworld"
ROUTE_METHOD="GET"
ROUTE_URL="/helloworld"
ROUTE_CREATEINGRESS="TRUE"
#####################################

(
    fission route delete --name $ROUTE_NAME
    fission fn delete --name $FN_NAME
    fission pkg delete --name $PKG_NAME
)