# Introduction

This project is used to black-box test local networks of nodes using the [PySys System test Framework](https://github.com/pysys-test/pysys-test).
PySys is an easy-to-use cross-platform test framework, providing a package of utility methods for process orchestration,
testcase management, concurrent testcase execution, and testcase validation. PySys is written in Python, and is supported
on both Python 2.7 and above. See the [PySys User Guide](https://github.com/pysys-test/pysys-test/blob/master/USERGUIDE.rst) for more details.

The tests run in the same manner as the [Behave framework](https://github.com/corda/behave), i.e. they download specific versions of the Corda jars from 
artifactory into a staging area, and can use external CENM environments (TestNet, Daywatch and Nightwatch), or run locally 
bootstrapped networks. Test CorDapps used are built from the [production-qa-cordapps](https://github.com/corda/production-qa-cordapps) 
repository. The repo is assumed by default to be cloned in the same parent directory and the CorDapps built as described in the 
project [README](https://github.com/corda/production-qa-cordapps/blob/master/README.md). This will be changed in the near future so that test 
CorDapps are downloaded from Artifactory.


# Dependencies

### Python 
If you are running on OSX do not use the bundled Python as this has restricted entitlements and will fail to load some libraries
(e.g. the Oracle client libraries). Instead use [Homebrew](https://brew.sh) and install python2 using `brew install python@2`. Once
installed the following packages should be installed using pip. Should you encounter any errors with pip installation, see further 
below for work arounds.

```
pip install pysys
pip install artifactory
pip install wget
pip install docker
pip install requests
pip install paramiko
pip install pyjks
pip install cx_Oracle
```

Should pip not be installed on the machine running the tests, pip can be installed using

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Should you not be able to install pyjks you may need to install the `build-essential` and `python-dev` packages on the 
machine. Install using;

```
sudo apt-get install build-essential
sudo apt-get install python-dev
```

You will need to install the 12.2 instant client and SDK packages in order to be able to use the cx_Oracle package. To install 
see the notes at [Oracle OSX](https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html), and 
[Oracle LINUX](https://www.oracle.com/uk/database/technologies/instant-client/linux-x86-64-downloads.html). Installation on ubuntu
will require the libaio1 pacakge installed using `sudo apt-get install libaio1`

  
## Docker
The framework makes use of Docker containers for database images when running Corda nodes against the non default H2 database. As
such the docker server needs to be [installed](https://docs.docker.com/v17.09/engine/installation/) on the host machine running the tests. 


## Environment variables

The following environment variables should be set;
```
CORDA_ARTIFACTORY_USERNAME -> username for corda enterprise artifactory account
CORDA_ARTIFACTORY_PASSWORD -> password for corda enterprise artifactory account 
DOCKER_USERNAME            -> username for docker
DOCKER_PASSWORD            -> password for docker
JAVA_HOME                  -> location of JDK 8
```

## Firewall rules

If running against external networks such as DayWatch, ports 12000 to 12999 must be open on the host machine for outside connections for
components in the external Corda network to communicate with Corda nodes started in each test.


# Setting up your IDEA

After cloning the repository, open IntelliJ and select to create a new Python project from the corda-test-pysys source tree. Once open,
in the project view open the module settings and ensure that the corda-test-pysys/src directory is added as a source directory. 


# Project structure

A summary overview of the project structure is shown below.
```
    ├── README.md
    ├── pysysproject.xml               # the pysys project file
    ├── resources                      # resources such as truststores and downloaded jars
    │   ├── keys
    │   └── staging
    ├── scripts                        # utilities
    │   ├── artifactory
    │   └── hsm
    ├── src                            # the pysys test extensions
    │   └── net
    └── test                           # the pysys test scenarios
        └── cordapps
            └── receiver
                └── receiver_cor_001   # an example testcase
                    ├── Input
                    ├── Output
                    ├── pysystest.xml
                    └── run.py

```


# Running a test

PySys has a launch script installed and put onto the path (pysys.py). The launch script can be used to print out tests, clean tests,
or to run tests. To see a full help usage use the -h option to either the top level script, or a particular run target, e.g.

```
# print help usage for available targets
pysys.py -h

# print help usage for the run target
pysys.py run -h

# run a given test by id
pysys.py run receiver_cor_001

# run tests in all supported modes
pysys.py run -m ALL 
```

Modes provide an easy mechanism to define ways in which a particular testcase can be run. For instance a mode can be defined for
each combination of Corda type (OS or ENT) and version thereof. Modes are defined in the `pysysdirconfig.xml` file and are applied
to each test scenario below this directory unless mode inheritance is disabled for a particular test. 


