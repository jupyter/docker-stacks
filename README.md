

[![Join the chat at https://gitter.im/Analyticsdojo/Analyticsdojo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Analyticsdojo/Analyticsdojo)

AnalyticsDojo is a data science community where you learn to data science and work on real projects. This repository contains a number of different sources of materials to use for analytics.

In order to get started with the Jupyter data science container, try the following command. 

**Note: You need to (a) download this directory and (b) change to the materials directory.**

```
docker run -d -p 8888:8888  -e GRANT_SUDO=yes  --name analyticsdojo  -v {enter path to materials directory}/materials/analyticsdojo:/home/jovyan/work jupyter/datascience-notebook start-notebook.sh
```
In the above command, you need to customize the location of the directory.  For example, on my machine it is the following:
```
docker run -d -p 8888:8888  -e GRANT_SUDO=yes  --name analyticsdojo  -v /Users/jasonkuruzovich/githubdesktop/materials/analyticsdojo:/home/jovyan/work jupyter/datascience-notebook start-notebook.sh
```
On a Windows machine, it might be the following:
```
docker run -d -p 8888:8888  -e GRANT_SUDO=yes  --name analyticsdojo  -v /C//Users/jkuruzovich/materials/analyticsdojo:/home/jovyan/work jupyter/datascience-notebook start-notebook.sh
```
If you reboot and later find that the container is not running, you can start it from the command line with 
```docker start analyticsdojo```

If you enter the wrong file path:

```
docker stop analyticsdojo
docker rm analyticsdojo 
```

Then rerun the command. 

This will launch a container (called analyticsdojo) and share the appropriate directory with the container.  This will allow the container to easily share files and notebooks with the operating system.

If everything is working correctly then  [http://localhost:8888/](http://localhost:8888/) will show the root directory of this repository in the Jupyter console.

![Console](http://i.imgur.com/0Jqvh56.png)

License
-------
Please check the individual directories regarding the licensing.  Because this project incorporates materials from different project, the subdirectories had different required attribuiton and licensing. 

