# Fission
This folder contains all files related to the Fission framework. 

Each file is designed to manage the environments efficiently, ensuring that the infrastructure is correctly set up or cleaned up as required by the project.

## Essencial Files/Folders

**./setupEnvs.sh**
- **Description**: This Bash script creates all necessary Fission environments for this project.
- **Usage**: Run this script as needed. If an environment already exists, an alert will be printed.
- **Notes**: Defining envs outside .sh file could result in weried bug (i.e. `fission env list` command will not show any thing). Thus, it is hard coded inside. If Fission env changes, need to also update ./deleteEnvs.sh


**./deleteEnvs.sh**
- **Description**: This Bash script deletes all environments from Fission.
- **Usage**: Run this script as needed to clean up all Fission environments.
- **Notes**: Defining envs outside .sh file could result in weried bug (i.e. `fission env list` command will not show any thing). Thus, it is hard coded inside. If Fission env changes, need to also update ./setupEnvs.sh

**./specs**
- **Description**: This folder contains yaml files for Fission.