## AntFarm

This repository provides and environment for running the Project 8 data acquisition.  It consists of two main components:
* Bash scripts to access the DAQ session
* Python scripts to control the modes of DAQ operation


### How to access the DAQ session

The DAQ session environment consists of two terminal panes. The top pane is for controling the DAQ operation, and the bottom pane shows the output from the DAQ software.

The session can be started with the `start_daq.sh` script:

    > /path/to/start_daq.sh

If a DAQ session is already running, you can attach to it with the `attach_daq.sh` script:

    > /path/to/attach_daq.sh

To disconnect your client from the DAQ session, use the `detach_daq.sh` script:

    > /path/to/detach_daq.sh

And finally, to stop the DAQ session, use the `stop_daq.sh` script:

    > /path/to/stop_daq.sh


### How to control the DAQ operation

There are three operating modes for the DAQ session:
* off -- nothing happens
* acquire -- mantis_server is running and ready to accept run requests
* rsync -- data is being synced with the specified destination

The script `switch_mode.py` should be used to change DAQ modes from the top pane of the DAQ session.

In the top pane of the DAQ session, the directory containing the scripts is added to the path, so you can execute those scripts without specifying a path.

To switch the DAQ mode to `off`:

    > switch_mode.py off

When switching the DAQ mode to `acquire`, you can optionally pass arguments to the `mantis_server`:

    > switch_mode.py acquire [optional parameters for mantis_server]

When switching the DAQ mode to `rsync`, you need to specify a json file with the information about the source and destination (see below):

    > switch_mode.py rsync [rsync_config.json]

### rsync configuration

When switching to rsync mode, a JSON-formatted configuration file must be supplied.  An example is provided in the `example` directory.  It consists of two main sections, `source` and `destination`.

```json
{
    "source":
    {
        "dirs":
        [
            "/some/other/dir1",
            "/some/other/dir2/"
        ]
    },
```

In the `source` section, the directories to be sycnronized with the destination are specified in an array. Using the standard from `rsync`, if a directory path ends with a forward slash (`/`), the contents of the directory will be copied to the `top-dir` of the destination; otherwise the directory itself (and its contents, of course) will be copied.

```json
    "destination":
    {
        "host": "my.server.com",
        "user": "me",
        "top-dir": "/data"
    }
}
```

In the `destination` section, there are three required components:
* `host` is the server location,
* `user` is the user that will be used to log into the host, and
* `top-dir` is the directory into which everything from the `source` will be copied.

### Other notes

* Two temporary files are created in the daq-session directory: `add_to_path.sh` and `status.json`. These should not be touched while a DAQ session is running.  Once the DAQ session is stopped, removing/modifying the files will have no effect.
* If the json in status.json becomes malformed and errors are produced by the python scripts, reset everything by deleting `status.json`, and stopping mantis_server or rsync, if either is in progress.
