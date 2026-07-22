#!/bin/bash
#########################################
#   Script used by pipeline to deploy   #
#     to DEV/UAT environments           #
#########################################
#
# Tell the script to fail if any errors occur.
# For commands which we don't mind failing, we will add "|| true"
set -e
#
## Variables
#
EXT_NAME=ckanorg
VENV=/var/www/sites/ckan.org
#
###########################################

## Functions
#
function pull_latest_ckan_code {
        echo "Beginning code update process..."
        
        # Set permissions to allow pipeline user to run the deployment
        sudo chown -R jumpbox-pipelines:ckan $VENV/

        # Check to see if the extension directory exists or not
        if [ -d $VENV/$EXT_NAME ]; then
          echo "Wagtail directory exists, proceeding."

          # Move into repository directory
          cd $VENV/$EXT_NAME/

          # Ensure the SSH remote is added to allow pipelines to pull code from BitBucket with key authentication (|| true added to avoid exiting on error if remote already exists)
          git remote add jumpbox-pipelines $BB_SSH_ORIGIN || true

          # Checkout the branch we are working with (in case somebody has been manually changing things)
          git checkout $BRANCH

          # Reset the repository in case, as above, manual changes have been made.
          git reset --hard
        else
          echo "The 'ckanorg' directory does not exist..."

          #cd $VENV/

          # Clone the repository
          #git clone $BB_SSH_ORIGIN

          # Move into the new extension directory
          #cd $VENV/src/$EXT_NAME/

          # Checkout the branch we are working with (in case somebody has been manually changing things)
          #git checkout $BRANCH
        fi

        # Pull the latest code
        git pull jumpbox-pipelines $BRANCH
}

function run_make_process {
        echo "Running post-deployment steps..."
        echo "Running 'manage.py collectstatic' command..."
        python manage.py collectstatic --noinput

        # Set ownership of virtual environment back to Nginx user
        sudo chown -R nginx:nginx $VENV
}

echo "Beginning deployment to $INSTANCE_TYPE..."

# Add BitBucket key fingerprint to avoid connection issues later
ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts

pull_latest_ckan_code
run_make_process

# Restart CKAN processes
case $INSTANCE_TYPE in
        WEB)
                # Restart uWSGI process
                echo "Restarting the uWSGI process..."
                sudo supervisorctl restart ckanorg:
                ;;
esac

echo "Deploymen complete."
