# HWRWebService

This repository contains code to produce a simple a web service for Handwriting Recognition. It uses
a Flask Web Server, Redis for queuing, and a Tensorflow backend.

## Dependencies

* Python
* Numpy
* Redis
* Redis-Py
* Flask
* Tensorflow
* Pillow
* HWR (BYU-Handwriting-Lab)

The easiest way to install is by using Conda. An environment.yaml file is included with the required
dependencies. The conda environment can be created and activated with the following commands:

```
conda env create -f environment.yaml
conda activate ws_hwr_env
```

## Usage

For this simple example, we need to start 3 processes:
* The Redis Server
* The Flask Web Server
* The Tensorflow Model Server

### Start the Servers

First, start the Redis Server by running the following script in the project's root directory:

```
sh ./start_redis.sh
```

Next, start the Flask Web Server

```
python webserver.py
```

Finally, start the Tensorflow Model Server

```
python hwrserver.py
```

### Run the Test App

Once we have started these 3 processes, we can now test out the Simple HWR Web Service. You can run this
test by executing the following command:

```
python testapp.py
```

### Configuration Settings

Settings can be changed in the `settings.py` file to change system and testing behavior.
