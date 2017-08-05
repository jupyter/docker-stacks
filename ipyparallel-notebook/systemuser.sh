#!/bin/sh
set -e
if getent passwd ${USER_ID} > /dev/null ; then
  echo "${USER} (${USER_ID}) exists"
else
  echo "Creating user ${USER} (${USER_ID})"
  useradd -u ${USER_ID} -m -d ${HOME} -s $SHELL ${USER}
fi

notebook_arg=""
if [ -n "${NOTEBOOK_DIR:+x}" ]
then
    notebook_arg="--notebook-dir=${NOTEBOOK_DIR}"
fi

echo create ipython profile

/tmp/profile/create_profile.sh -f /tmp/profile/profiles

sudo chown -R ${USER} ${HOME}/.ipython

# update pip source
sudo -u ${USER} mkdir -p ${HOME}/.pip && \
echo "[global]" > ${HOME}/.pip/pip.conf && \
echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ${HOME}/.pip/pip.conf && \
echo "" >> ${HOME}/.pip/pip.conf && \
echo "[install]" >> ${HOME}/.pip/pip.conf && \
echo "trusted-host=mirrors.aliyun.com" >> ${HOME}/.pip/pip.conf

sudo -E PATH="${CONDA_DIR}/bin:$PATH" -E CONDA_ENVS_PATH="${HOME}/.conda/envs" \
  -u ${USER} ${CONDA_DIR}/bin/jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=${JPY_USER} \
  --cookie-name=${JPY_COOKIE_NAME} \
  --base-url=${JPY_BASE_URL} \
  --hub-prefix=${JPY_HUB_PREFIX} \
  --hub-api-url=${JPY_HUB_API_URL} \
  ${notebook_arg} \
  $@
