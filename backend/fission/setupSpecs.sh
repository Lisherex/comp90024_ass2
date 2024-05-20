#!/bin/bash

# Get the current script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if the specs directory exists
if [ ! -d "$DIR/specs" ]; then
    echo "specs directory does not exist"
    (
        cd "$DIR"
        fission specs init
    )
else
    echo "specs directory exists"
fi

# Create Fission environment YAML files
(
    cd "$DIR"
    FISSION_NAMESPACE=default
    declare -A envs
    envs["python"]="fission/python-env-3.9 fission/python-builder-3.9"
    # envs["nodejs"]="fission/node-env fission/node-builder"

    for env in "${!envs[@]}"; do
        config=(${envs[$env]})
        image="${config[0]}"
        builder="${config[1]}"

        # Check if the environment already exists
        if fission env get --name "$env" --namespace "$FISSION_NAMESPACE" > /dev/null 2>&1; then
            echo "Environment $env already exists, skipping creation..."
        else
            fission env create --spec --name "$env" --image "$image" --builder "$builder" --namespace "$FISSION_NAMESPACE"
            echo "Environment $env created."
        fi
    done
)

# Iterate over each subdirectory in the functions directory
FUNSDIR="$DIR/functions"
for folder in "$FUNSDIR"/*/; do
    # Check if the spec.txt file exists
    if [ -f "$folder/spec.txt" ]; then
        echo "Reading $folder/spec.txt..."

        # Initialize variables
        unset FISSION_NAMESPACE ENV_NAME PKG_NAME FN_NAME FN_ENTRYPOINT ROUTE_NAME ROUTE_METHOD ROUTE_URL ROUTE_CREATEINGRESS

        # Read spec.txt file content
        while IFS='=' read -r key value; do
            value=$(echo $value | tr -d '"')
            case "$key" in
                "FISSION_NAMESPACE") FISSION_NAMESPACE="$value" ;;
                "ENV_NAME") ENV_NAME="$value" ;;
                "PKG_NAME") PKG_NAME="$value" ;;
                "FN_NAME") FN_NAME="$value" ;;
                "FN_ENTRYPOINT") FN_ENTRYPOINT="$value" ;;
                "ROUTE_NAME") ROUTE_NAME="$value" ;;
                "ROUTE_METHOD") ROUTE_METHOD="$value" ;;
                "ROUTE_URL") ROUTE_URL="$value" ;;
                "ROUTE_CREATEINGRESS") ROUTE_CREATEINGRESS="$value" ;;
            esac
        done < "$folder/spec.txt"
        
        # Compress the folder contents into a zip file
        zip_file="${folder%/}/${FN_NAME}.zip"
        echo "Compressing $folder to $zip_file..."
        (
            cd "$folder"
            zip -r "$zip_file" * -x spec.txt "$zip_file"
        )

        echo "$folder compressed."
        relative_zip_file="./${zip_file#"$DIR/"}"

        # Create Fission package
        echo "Create Fission package"
        fission package create --spec --name "$PKG_NAME" --sourcearchive "$relative_zip_file" --env "$ENV_NAME" --buildcmd "./build.sh" --namespace "$FISSION_NAMESPACE"
        echo""

        # Create Fission function
        echo "Create Fission function"
        fission fn create --spec --name "$FN_NAME" --env "$ENV_NAME" --pkg "$PKG_NAME" --entrypoint "$FN_ENTRYPOINT" --namespace "$FISSION_NAMESPACE" --configmap api-urls --configmap internal-service-ports --secret auth
        echo""

        # Create Fission route
        echo "Create Fission route"
        if [ "$ROUTE_CREATEINGRESS" = "TRUE" ]; then
            fission route create --spec --name "$ROUTE_NAME" --method $ROUTE_METHOD --url "$ROUTE_URL" --function "$FN_NAME" --namespace "$FISSION_NAMESPACE" --createingress
        else
            fission route create --spec --name "$ROUTE_NAME" --method $ROUTE_METHOD --url "$ROUTE_URL" --function "$FN_NAME" --namespace "$FISSION_NAMESPACE"
        fi
        echo""
    else
        echo "$folder/spec.txt file does not exist, skipping..."
    fi
    echo""
    echo""
    echo""
done