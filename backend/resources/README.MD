# Resources

This folder contains snapshots of resources by namespace.

# Usage: Update snapshots
- `source ./pull.sh <target-namespace>`
    - All yaml files will be saved under **.\/\<target-namespace\>**. Forward k8s ports on your local machine before running this script.
    - resource_types=("deployments" "pods" "services" "configmaps" "secrets" "ingresses" "pvc" "statefulsets" "daemonsets" "jobs" "cronjobs")
