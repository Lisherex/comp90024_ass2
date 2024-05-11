#!/bin/bash
set -e

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

# ref: fission env create --spec --name python --image fission/python-env --builder fission/python-builder
(
    FISSION_NAMESPACE=default
    declare -A envs
    envs["python"]="fission/python-env-3.9 fission/python-builder-3.9"
    envs["nodejs"]="fission/node-env fission/node-builder"

    # check if env exists; otherwise create
    for env in "${!envs[@]}"; do
        config=(${envs[$env]})
        image="${config[0]}"
        builder="${config[1]}"

        env_exists=$(fission env get --name $env --namespace $FISSION_NAMESPACE 2>&1 || echo "not found")

        if [[ "$env_exists" == *"not found"* ]]; then
            echo "$env environment does not exist. Creating now..."
            fission env create --name $env --image $image --builder $builder --namespace $FISSION_NAMESPACE
        else
            echo "$env environment already exists."
        fi
        echo ""
    done

)