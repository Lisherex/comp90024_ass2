#!/bin/bash
# ./pull.sh my-namespace
NAMESPACE=$1

# List of resource types to save
resource_types=("deployments" "pods" "services" "configmaps" "secrets" "ingresses" "pvc" "statefulsets" "daemonsets" "jobs" "cronjobs")

# Check if namespace is provided
if [ -z "$NAMESPACE" ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

# Function to save YAML configuration of a resource type
save_yaml() {
    local resource_type=$1
    local resource_names=$(kubectl get $resource_type -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')
    
    if [ -n "$resource_names" ]; then
        # Create directory for the resource type if it doesn't exist
        mkdir -p $NAMESPACE/$resource_type
        
        for resource_name in $resource_names; do
            kubectl get $resource_type $resource_name -n $NAMESPACE -o yaml > ${NAMESPACE}/${resource_type}/${resource_name}.yaml
            echo "Saved $resource_name configuration to ${NAMESPACE}/${resource_type}/${resource_name}.yaml"
        done
    else
        echo "No $resource_type found in namespace $NAMESPACE"
    fi
}


# Save YAML configurations for all listed resource types
for resource_type in "${resource_types[@]}"; do
    save_yaml $resource_type
done