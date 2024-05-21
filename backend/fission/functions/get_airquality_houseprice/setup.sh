#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

#####################################
FISSION_NAMESPACE=default

ENV_NAME="python"

PKG_NAME="get-airquality-houseprice"

FN_NAME="get-airquality-houseprice"
FN_ENTRYPOINT="get_airquality_houseprice.main"

ROUTE_NAME="airquality-houseprice"
ROUTE_METHOD="GET"
ROUTE_URL="/airquality/houseprice"
ROUTE_CREATEINGRESS="TRUE"
#####################################

(
    fission route delete --name $ROUTE_NAME
    fission fn delete --name $FN_NAME
    fission pkg delete --name $PKG_NAME
)

(
    pushd "$DIR"
    zip -r upload.zip * -x setup.sh
    popd
)

(
    if fission package info --name $PKG_NAME --namespace $FISSION_NAMESPACE &>/dev/null; then
        fission package update --name $PKG_NAME --sourcearchive $DIR/upload.zip --env $ENV_NAME --buildcmd "./build.sh" --namespace $FISSION_NAMESPACE
    else
        fission package create --name $PKG_NAME --sourcearchive $DIR/upload.zip --env $ENV_NAME --buildcmd "./build.sh" --namespace $FISSION_NAMESPACE
    fi

    if fission fn get --name $FN_NAME --namespace $FISSION_NAMESPACE &>/dev/null; then
        fission fn update --name $FN_NAME --env $ENV_NAME --pkg $PKG_NAME --entrypoint $FN_ENTRYPOINT --namespace $FISSION_NAMESPACE --configmap api-urls --configmap internal-service-ports --secret auth
    else
        fission fn create --name $FN_NAME --env $ENV_NAME --pkg $PKG_NAME --entrypoint $FN_ENTRYPOINT --namespace $FISSION_NAMESPACE --configmap api-urls --configmap internal-service-ports --secret auth
    fi

    if fission route get --name $ROUTE_NAME --namespace $FISSION_NAMESPACE &>/dev/null; then
        if [ "$ROUTE_CREATEINGRESS" = "TRUE" ]; then
            fission route update --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE --createingress
        else
            fission route update --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE
        fi
    else
        if [ "$ROUTE_CREATEINGRESS" = "TRUE" ]; then
            fission route create --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE --createingress
        else
            fission route create --name $ROUTE_NAME --method $ROUTE_METHOD --url $ROUTE_URL --function $FN_NAME --namespace $FISSION_NAMESPACE
        fi
    fi

    rm "${DIR}/upload.zip"
)