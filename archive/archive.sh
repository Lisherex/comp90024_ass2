#!/bin/bash
(
    FISSION_NAMESPACE=default
    fission route delete --name helloworld
    fission fn delete --name helloworld
    fission pkg delete --name helloworld
    
    

    # package helloWorld
    # fission package create --spec --src functions/helloworld/ --env python --name helloworld --namespace $FISSION_NAMESPACE
    # fission package update --spec --src functions/helloworld/ --env python --name helloworld --namespace $FISSION_NAMESPACE
    fission package create --src functions/helloworld/ --env python --name helloworld --namespace $FISSION_NAMESPACE
    # fission package create --src functions/helloworld.zip --env python --name helloworld --namespace $FISSION_NAMESPACE

    # create/update function
    # fission fn create --spec --name helloworld --env python --pkg helloworld --entrypoint main --namespace $FISSION_NAMESPACE
    # fission fn update --spec --name helloworld --env python --pkg helloworld --entrypoint main --namespace $FISSION_NAMESPACE
    fission fn create --name helloworld --env python --pkg helloworld --entrypoint "helloworld.main" --namespace $FISSION_NAMESPACE

    # create router (api)
    # fission route create --spec --name helloworld --method GET --url /helloworld --function helloworld --namespace $FISSION_NAMESPACE  --createingress
    # fission route update --spec --name helloworld --method GET --url /helloworld --function helloworld --namespace $FISSION_NAMESPACE
    fission route create --name helloworld --method GET --url /helloworld --function helloworld --namespace $FISSION_NAMESPACE --createingress

    # deploy
    # fission spec apply

    echo "Deployment complete."
)

