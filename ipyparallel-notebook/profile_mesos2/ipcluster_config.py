# Configuration file for ipcluster.

# ------------------------------------------------------------------------------
# Application(SingletonConfigurable) configuration
# ------------------------------------------------------------------------------

## This is an application.

## The date format used by logging formatters for %(asctime)s
# c.Application.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
# c.Application.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
# c.Application.log_level = 30

# ------------------------------------------------------------------------------
# BaseIPythonApplication(Application) configuration
# ------------------------------------------------------------------------------

## IPython: an enhanced interactive Python shell.

## Whether to create profile dir if it doesn't exist
# c.BaseIPythonApplication.auto_create = False

## Whether to install the default config files into the profile dir. If a new
#  profile is being created, and IPython contains config files for that profile,
#  then they will be staged into the new directory.  Otherwise, default config
#  files will be automatically generated.
# c.BaseIPythonApplication.copy_config_files = False

## Path to an extra config file to load.
#  
#  If specified, load this config file in addition to any other IPython config.
# c.BaseIPythonApplication.extra_config_file = u''

## The name of the IPython directory. This directory is used for logging
#  configuration (through profiles), history storage, etc. The default is usually
#  $HOME/.ipython. This option can also be specified through the environment
#  variable IPYTHONDIR.
# c.BaseIPythonApplication.ipython_dir = u''

## Whether to overwrite existing config files when copying
# c.BaseIPythonApplication.overwrite = False

## The IPython profile to use.
# c.BaseIPythonApplication.profile = u'default'

## Create a massive crash report when IPython encounters what may be an internal
#  error.  The default is to append a short message to the usual traceback
# c.BaseIPythonApplication.verbose_crash = False

# ------------------------------------------------------------------------------
# BaseParallelApplication(BaseIPythonApplication) configuration
# ------------------------------------------------------------------------------

## IPython: an enhanced interactive Python shell.

## whether to cleanup old logfiles before starting
# c.BaseParallelApplication.clean_logs = False

## String id to add to runtime files, to prevent name collisions when using
#  multiple clusters with a single profile simultaneously.
#  
#  When set, files will be named like: 'ipcontroller-<cluster_id>-engine.json'
#  
#  Since this is text inserted into filenames, typical recommendations apply:
#  Simple character strings are ideal, and spaces are not recommended (but should
#  generally work).
# c.BaseParallelApplication.cluster_id = ''

## whether to log to a file
# c.BaseParallelApplication.log_to_file = False

## The ZMQ URL of the iplogger to aggregate logging.
# c.BaseParallelApplication.log_url = ''

## Set the working dir for the process.
# c.BaseParallelApplication.work_dir = u'/home/xinge'

# ------------------------------------------------------------------------------
# IPClusterEngines(BaseParallelApplication) configuration
# ------------------------------------------------------------------------------

## Daemonize the ipcluster program. This implies --log-to-file. Not available on
#  Windows.
# c.IPClusterEngines.daemonize = False

## The timeout (in seconds)
# c.IPClusterEngines.early_shutdown = 30

## Deprecated, use engine_launcher_class
# c.IPClusterEngines.engine_launcher = None

## The class for launching a set of Engines. Change this value to use various
#  batch systems to launch your engines, such as PBS,SGE,MPI,etc. Each launcher
#  class has its own set of configuration options, for making sure it will work
#  in your environment.
#  
#  You can also write your own launcher, and specify it's absolute import path,
#  as in 'mymodule.launcher.FTLEnginesLauncher`.
#  
#  IPython's bundled examples include:
#  
#      Local : start engines locally as subprocesses [default]
#      MPI : use mpiexec to launch engines in an MPI environment
#      PBS : use PBS (qsub) to submit engines to a batch queue
#      SGE : use SGE (qsub) to submit engines to a batch queue
#      LSF : use LSF (bsub) to submit engines to a batch queue
#      SSH : use SSH to start the controller
#                  Note that SSH does *not* move the connection files
#                  around, so you will likely have to do this manually
#                  unless the machines are on a shared file system.
#      HTCondor : use HTCondor to submit engines to a batch queue
#      Slurm : use Slurm to submit engines to a batch queue
#      WindowsHPC : use Windows HPC
#  
#  If you are using one of IPython's builtin launchers, you can specify just the
#  prefix, e.g:
#  
#      c.IPClusterEngines.engine_launcher_class = 'SSH'
#  
#  or:
#  
#      ipcluster start --engines=MPI
# c.IPClusterEngines.engine_launcher_class = 'LocalEngineSetLauncher'

## The number of engines to start. The default is to use one for each CPU on your
#  machine
# c.IPClusterEngines.n = 4

# ------------------------------------------------------------------------------
# IPClusterStart(IPClusterEngines) configuration
# ------------------------------------------------------------------------------

## whether to create the profile_dir if it doesn't exist
# c.IPClusterStart.auto_create = True

## whether to cleanup old logs before starting
# c.IPClusterStart.clean_logs = True

## Set the IP address of the controller.
# c.IPClusterStart.controller_ip = u''

## Deprecated, use controller_launcher_class
# c.IPClusterStart.controller_launcher = None

## The class for launching a Controller. Change this value if you want your
#  controller to also be launched by a batch system, such as PBS,SGE,MPI,etc.
#  
#  Each launcher class has its own set of configuration options, for making sure
#  it will work in your environment.
#  
#  Note that using a batch launcher for the controller *does not* put it in the
#  same batch job as the engines, so they will still start separately.
#  
#  IPython's bundled examples include:
#  
#      Local : start engines locally as subprocesses
#      MPI : use mpiexec to launch the controller in an MPI universe
#      PBS : use PBS (qsub) to submit the controller to a batch queue
#      SGE : use SGE (qsub) to submit the controller to a batch queue
#      LSF : use LSF (bsub) to submit the controller to a batch queue
#      HTCondor : use HTCondor to submit the controller to a batch queue
#      Slurm : use Slurm to submit engines to a batch queue
#      SSH : use SSH to start the controller
#      WindowsHPC : use Windows HPC
#  
#  If you are using one of IPython's builtin launchers, you can specify just the
#  prefix, e.g:
#  
#      c.IPClusterStart.controller_launcher_class = 'SSH'
#  
#  or:
#  
#      ipcluster start --controller=MPI
# c.IPClusterStart.controller_launcher_class = 'LocalControllerLauncher'

## delay (in s) between starting the controller and the engines
# c.IPClusterStart.delay = 1.0

## Whether to reset config files as part of '--create'.
# c.IPClusterStart.reset = False

# ------------------------------------------------------------------------------
# ProfileDir(LoggingConfigurable) configuration
# ------------------------------------------------------------------------------

## An object to manage the profile directory and its resources.
#  
#  The profile directory is used by all IPython applications, to manage
#  configuration, logging and security.
#  
#  This object knows how to find, create and manage these directories. This
#  should be used by any code that wants to handle profiles.

## Set the profile location directly. This overrides the logic used by the
#  `profile` option.
# c.ProfileDir.location = u''

# ------------------------------------------------------------------------------
# LocalEngineSetLauncher(LocalEngineLauncher) configuration
# ------------------------------------------------------------------------------

## Launch a set of engines as regular external processes.

## delay (in seconds) between starting each engine after the first. This can help
#  force the engines to get their ids in order, or limit process flood when
#  starting many engines.
# c.LocalEngineSetLauncher.delay = 0.1

# ------------------------------------------------------------------------------
# MPILauncher(LocalProcessLauncher) configuration
# ------------------------------------------------------------------------------

## Launch an external process using mpiexec.

## The command line arguments to pass to mpiexec.
# c.MPILauncher.mpi_args = []

## The mpiexec command to use in starting the process.
# c.MPILauncher.mpi_cmd = ['mpiexec']

# ------------------------------------------------------------------------------
# MPIControllerLauncher(MPILauncher,ControllerMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using mpiexec.

# ------------------------------------------------------------------------------
# MPIEngineSetLauncher(MPILauncher,EngineMixin) configuration
# ------------------------------------------------------------------------------

## Launch engines using mpiexec

# ------------------------------------------------------------------------------
# SSHLauncher(LocalProcessLauncher) configuration
# ------------------------------------------------------------------------------

## A minimal launcher for ssh.
#  
#  To be useful this will probably have to be extended to use the ``sshx`` idea
#  for environment variables.  There could be other things this needs as well.

## hostname on which to launch the program
# c.SSHLauncher.hostname = ''

## user@hostname location for ssh in one setting
# c.SSHLauncher.location = ''

## args to pass to scp
# c.SSHLauncher.scp_args = []

## command for sending files
# c.SSHLauncher.scp_cmd = ['scp']

## args to pass to ssh
# c.SSHLauncher.ssh_args = ['-tt']

## command for starting ssh
# c.SSHLauncher.ssh_cmd = ['ssh']

## List of (remote, local) files to fetch after starting
# c.SSHLauncher.to_fetch = []

## List of (local, remote) files to send before starting
# c.SSHLauncher.to_send = []

## username for ssh
# c.SSHLauncher.user = ''

# ------------------------------------------------------------------------------
# SSHClusterLauncher(SSHLauncher,ClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## The remote profile_dir to use.
#  
#  If not specified, use calling profile, stripping out possible leading homedir.
# c.SSHClusterLauncher.remote_profile_dir = ''

# ------------------------------------------------------------------------------
# SSHControllerLauncher(SSHClusterLauncher,ControllerMixin) configuration
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# SSHEngineLauncher(SSHClusterLauncher,EngineMixin) configuration
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# SSHEngineSetLauncher(LocalEngineSetLauncher) configuration
# ------------------------------------------------------------------------------

## dict of engines to launch.  This is a dict by hostname of ints, corresponding
#  to the number of engines to start on that host.
# c.SSHEngineSetLauncher.engines = {}

# ------------------------------------------------------------------------------
# SSHProxyEngineSetLauncher(SSHClusterLauncher) configuration
# ------------------------------------------------------------------------------

## Launcher for calling `ipcluster engines` on a remote machine.
#  
#  Requires that remote profile is already configured.

## 
# c.SSHProxyEngineSetLauncher.ipcluster_cmd = ['ipcluster']

# ------------------------------------------------------------------------------
# WindowsHPCLauncher(BaseLauncher) configuration
# ------------------------------------------------------------------------------

## The command for submitting jobs.
# c.WindowsHPCLauncher.job_cmd = 'job'

## The filename of the instantiated job script.
# c.WindowsHPCLauncher.job_file_name = u'ipython_job.xml'

## A regular expression used to get the job id from the output of the
#  submit_command.
# c.WindowsHPCLauncher.job_id_regexp = '\\d+'

## The hostname of the scheduler to submit the job to.
# c.WindowsHPCLauncher.scheduler = ''

# ------------------------------------------------------------------------------
# WindowsHPCControllerLauncher(WindowsHPCLauncher,ClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## WinHPC xml job file.
# c.WindowsHPCControllerLauncher.job_file_name = u'ipcontroller_job.xml'

# ------------------------------------------------------------------------------
# WindowsHPCEngineSetLauncher(WindowsHPCLauncher,ClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## jobfile for ipengines job
# c.WindowsHPCEngineSetLauncher.job_file_name = u'ipengineset_job.xml'

# ------------------------------------------------------------------------------
# BatchSystemLauncher(BaseLauncher) configuration
# ------------------------------------------------------------------------------

## Launch an external process using a batch system.
#  
#  This class is designed to work with UNIX batch systems like PBS, LSF,
#  GridEngine, etc.  The overall model is that there are different commands like
#  qsub, qdel, etc. that handle the starting and stopping of the process.
#  
#  This class also has the notion of a batch script. The ``batch_template``
#  attribute can be set to a string that is a template for the batch script. This
#  template is instantiated using string formatting. Thus the template can use
#  {n} fot the number of instances. Subclasses can add additional variables to
#  the template dict.

## The filename of the instantiated batch script.
# c.BatchSystemLauncher.batch_file_name = u'batch_script'

## The string that is the batch script template itself.
# c.BatchSystemLauncher.batch_template = ''

## The file that contains the batch template.
# c.BatchSystemLauncher.batch_template_file = u''

## The name of the command line program used to delete jobs.
# c.BatchSystemLauncher.delete_command = ['']

## A regular expression used to get the job id from the output of the
#  submit_command.
# c.BatchSystemLauncher.job_id_regexp = ''

## The group we wish to match in job_id_regexp (0 to match all)
# c.BatchSystemLauncher.job_id_regexp_group = 0

## The batch queue.
# c.BatchSystemLauncher.queue = u''

## The name of the command line program used to submit jobs.
# c.BatchSystemLauncher.submit_command = ['']

# ------------------------------------------------------------------------------
# PBSLauncher(BatchSystemLauncher) configuration
# ------------------------------------------------------------------------------

## A BatchSystemLauncher subclass for PBS.

## The PBS delete command ['qdel']
# c.PBSLauncher.delete_command = ['qdel']

## Regular expresion for identifying the job ID [r'\d+']
# c.PBSLauncher.job_id_regexp = '\\d+'

## The PBS submit command ['qsub']
# c.PBSLauncher.submit_command = ['qsub']

# ------------------------------------------------------------------------------
# PBSControllerLauncher(PBSLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using PBS.

## batch file name for the controller job.
# c.PBSControllerLauncher.batch_file_name = u'pbs_controller'

# ------------------------------------------------------------------------------
# PBSEngineSetLauncher(PBSLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch Engines using PBS

## batch file name for the engine(s) job.
# c.PBSEngineSetLauncher.batch_file_name = u'pbs_engines'

# ------------------------------------------------------------------------------
# SlurmLauncher(BatchSystemLauncher) configuration
# ------------------------------------------------------------------------------

## A BatchSystemLauncher subclass for slurm.

## Slurm account to be used
# c.SlurmLauncher.account = u''

## The slurm delete command ['scancel']
# c.SlurmLauncher.delete_command = ['scancel']

## Regular expresion for identifying the job ID [r'\d+']
# c.SlurmLauncher.job_id_regexp = '\\d+'

## Extra Slurm options
# c.SlurmLauncher.options = u''

## Slurm QoS to be used
# c.SlurmLauncher.qos = u''

## The slurm submit command ['sbatch']
# c.SlurmLauncher.submit_command = ['sbatch']

## Slurm timelimit to be used
# c.SlurmLauncher.timelimit = u''

# ------------------------------------------------------------------------------
# SlurmControllerLauncher(SlurmLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using Slurm.

## batch file name for the controller job.
# c.SlurmControllerLauncher.batch_file_name = u'slurm_controller.sbatch'

# ------------------------------------------------------------------------------
# SlurmEngineSetLauncher(SlurmLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch Engines using Slurm

## batch file name for the engine(s) job.
# c.SlurmEngineSetLauncher.batch_file_name = u'slurm_engine.sbatch'

# ------------------------------------------------------------------------------
# SGELauncher(PBSLauncher) configuration
# ------------------------------------------------------------------------------

## Sun GridEngine is a PBS clone with slightly different syntax

# ------------------------------------------------------------------------------
# SGEControllerLauncher(SGELauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using SGE.

## batch file name for the ipontroller job.
# c.SGEControllerLauncher.batch_file_name = u'sge_controller'

# ------------------------------------------------------------------------------
# SGEEngineSetLauncher(SGELauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch Engines with SGE

## batch file name for the engine(s) job.
# c.SGEEngineSetLauncher.batch_file_name = u'sge_engines'

# ------------------------------------------------------------------------------
# LSFLauncher(BatchSystemLauncher) configuration
# ------------------------------------------------------------------------------

## A BatchSystemLauncher subclass for LSF.

## The PBS delete command ['bkill']
# c.LSFLauncher.delete_command = ['bkill']

## Regular expresion for identifying the job ID [r'\d+']
# c.LSFLauncher.job_id_regexp = '\\d+'

## The PBS submit command ['bsub']
# c.LSFLauncher.submit_command = ['bsub']

# ------------------------------------------------------------------------------
# LSFControllerLauncher(LSFLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using LSF.

## batch file name for the controller job.
# c.LSFControllerLauncher.batch_file_name = u'lsf_controller'

# ------------------------------------------------------------------------------
# LSFEngineSetLauncher(LSFLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch Engines using LSF

## batch file name for the engine(s) job.
# c.LSFEngineSetLauncher.batch_file_name = u'lsf_engines'

# ------------------------------------------------------------------------------
# HTCondorLauncher(BatchSystemLauncher) configuration
# ------------------------------------------------------------------------------

## A BatchSystemLauncher subclass for HTCondor.
#  
#  HTCondor requires that we launch the ipengine/ipcontroller scripts rather that
#  the python instance but otherwise is very similar to PBS.  This is because
#  HTCondor destroys sys.executable when launching remote processes - a launched
#  python process depends on sys.executable to effectively evaluate its module
#  search paths. Without it, regardless of which python interpreter you launch
#  you will get the to built in module search paths.
#  
#  We use the ip{cluster, engine, controller} scripts as our executable to
#  circumvent this - the mechanism of shebanged scripts means that the python
#  binary will be launched with argv[0] set to the *location of the ip{cluster,
#  engine, controller} scripts on the remote node*. This means you need to take
#  care that:
#  
#  a. Your remote nodes have their paths configured correctly, with the ipengine and ipcontroller
#     of the python environment you wish to execute code in having top precedence.
#  b. This functionality is untested on Windows.
#  
#  If you need different behavior, consider making you own template.

## The HTCondor delete command ['condor_rm']
# c.HTCondorLauncher.delete_command = ['condor_rm']

## Regular expression for identifying the job ID [r'(\d+)\.$']
# c.HTCondorLauncher.job_id_regexp = '(\\d+)\\.$'

## The group we wish to match in job_id_regexp [1]
# c.HTCondorLauncher.job_id_regexp_group = 1

## The HTCondor submit command ['condor_submit']
# c.HTCondorLauncher.submit_command = ['condor_submit']

# ------------------------------------------------------------------------------
# HTCondorControllerLauncher(HTCondorLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch a controller using HTCondor.

## batch file name for the controller job.
# c.HTCondorControllerLauncher.batch_file_name = u'htcondor_controller'

# ------------------------------------------------------------------------------
# HTCondorEngineSetLauncher(HTCondorLauncher,BatchClusterAppMixin) configuration
# ------------------------------------------------------------------------------

## Launch Engines using HTCondor

## batch file name for the engine(s) job.
# c.HTCondorEngineSetLauncher.batch_file_name = u'htcondor_engines'

# Required
# MUST SET
import os

user = os.environ.get("JPY_USER", "xinge")

# url with port to a marathon master
c.MarathonLauncher.marathon_master_url = os.environ.get("MARATHON_MASTER_URL",
                                                        'http://192.168.0.100:8080')
# Marathon application group. These needs to be unique per a cluster so if you have multiple users deploying clusters
# make sure they choose their own application group.
c.MarathonLauncher.marathon_app_group = '/ipyparallel/' + user

# Resonable defaults
c.IPClusterStart.controller_launcher_class = 'ipyparallel_mesos.launcher.MarathonControllerLauncher'
c.IPClusterEngines.engine_launcher_class = 'ipyparallel_mesos.launcher.MarathonEngineSetLauncher'

# Docker container image for the controller
c.MarathonLauncher.controller_docker_image = os.environ.get("CONTROLLER_DOCKER_IMAGE",
                                                            'registry.fxdayu.com/ipyparallel-marathon-controller:1.0')
# Docker image for the engine. This is where you should install custom dependencies
c.MarathonLauncher.engine_docker_image = os.environ.get("ENGINE_DOCKER_IMAGE",
                                                        'registry.fxdayu.com/ipyparallel-marathon-engine:1.0')

# Optional
c.MarathonLauncher.engine_memory = 512  # Amount of memory (in megabytes) to limit the docker container. NOTE: if your engine uses more the this, the docker container will be killed by the kernel without warning.
c.MarathonLauncher.controller_memory = 512  # Amount of memory (in megabytes) to limit the docker container. NOTE: if your engine uses more the this, the docker container will be killed by the kernel without warning.
c.MarathonLauncher.controller_config_port = '1235'  # The port the controller exposes for clients and engines to retrive connection information. Note, if there are multiple users on the same cluster this will need to be changed
c.MarathonLauncher.engine_docker_env = {
    "MARATHON_APP_GROUP": user,
    "PYTHONPATH": "/data/site-packages:$PYTHONPATH"
}
c.MarathonLauncher.engine_docker_volumes = [
    {
        "HostPath": "/data/user/" + os.environ.get("$JPY_USER") + "/work",
        "ContainerPath": "/data/site-packages",
        "Mode": "ro"
    }
]
