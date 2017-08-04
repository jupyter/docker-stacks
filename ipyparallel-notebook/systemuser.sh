#!/bin/sh
set -e
if getent passwd $USER_ID > /dev/null ; then
  echo "$USER ($USER_ID) exists"
else
  echo "Creating user $USER ($USER_ID)"
  useradd -u $USER_ID -s $SHELL $USER
fi

notebook_arg=""
if [ -n "${NOTEBOOK_DIR:+x}" ]
then
    notebook_arg="--notebook-dir=${NOTEBOOK_DIR}"
fi

echo create ipython profile

/tmp/profile/create_profile.sh -f /tmp/profile/profiles

sudo chown -R ${USER} ~/.ipython

sudo -E PATH="${CONDA_DIR}/bin:$PATH" -u $USER $CONDA_DIR/bin/jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL \
  ${notebook_arg} \
  $@
