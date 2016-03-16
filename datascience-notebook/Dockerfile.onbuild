FROM  jupyter/datascience-notebook

ONBUILD COPY . /home/jovyan/work

ONBUILD RUN  ( [ -e requirements.txt ] && pip install --no-cache-dir -r requirements.txt ) || true

ONBUILD RUN  ( [ -e environment.yml ] && conda install --file environment.yml ) || true
