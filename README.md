## daq-session

This repository consists of two main components:
* Bash scripts to access the DAQ session
* Python scripts to control the modes of DAQ operation


### How to access the DAQ session

The DAQ session environment consists of two terminal panes. The top pane is for controling the DAQ operation, and the bottom pane shows the output from the DAQ software.

The session can be started with the `start_daq.sh` script:
    > ./start_daq.sh

If a DAQ session is already running, you can attach to it with the `attach_daq.sh` script:
    > ./attach_daq.sh

To disconnect your client from the DAQ session, use the `detach_daq.sh` script:
    > ./detach_daq.sh

And finally, to stop the DAQ session, use the `stop_daq.sh` script:
    > ./stop_daq.sh


### How to control the DAQ operation

There are three operating modes for the DAQ session:
* off -- nothing happens
* acquire -- mantis_server is running and ready to accept run requests
* rsync -- data is being synced with the specified destination

The script `switch_mode.py` should be used to change DAQ modes from the top pane of the DAQ session.

To switch the DAQ mode to `off`:
    > python switch_mode.py off

When switching the DAQ mode to `acquire`, you can optionally pass arguments to the `mantis_server`:
    > python switch_mode.py acquire [optional parameters for mantis_server]

When switching the DAQ mode to `rsync`, you need to specify a json file with the information about the destination:
    > python switch_mode.py rsync [dest_info.json]

Two helper scripts are used in addition to `swtich_mode.py`: `start_acquire.py` and `start_rsync.py`. These should not be used directly.