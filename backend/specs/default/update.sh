set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

kubectl apply -f ${DIR}/configMap.yaml

kubectl apply -f ${DIR}/mySecrets.yaml