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

# (
#     fission route delete --name $ROUTE_NAME
#     fission fn delete --name $FN_NAME
#     fission pkg delete --name $PKG_NAME
# )

(
    pushd "$DIR"
    zip -r upload.zip * -x setup.sh
    popd
)

(
    fission package create --name $PKG_NAME --sourcearchive $DIR/upload.zip --env $ENV_NAME --buildcmd "./build.sh" --namespace $FISSION_NAMESPACE
    fission fn create --name $FN_NAME --env $ENV_NAME --pkg $PKG_NAME --entrypoint $FN_ENTRYPOINT --namespace $FISSION_NAMESPACE

    if [ "$ROUTE_CREATEINGRESS" = "TRUE" ]; then
        fission route create --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE --createingress
    else
        fission route create --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE
    fi

    rm "${DIR}/upload.zip"
)