from jupyter/datascience-notebook


ONBUILD COPY requirements.txt /usr/src/app/

ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /home/jovyan/work