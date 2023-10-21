# ArUco Queue

## Overview

This component can be used to stack together multiple [ArUco Detector](https://github.com/miguelscarv/aruco-detector) outputs by default. It uses a simple Python list to join all the outputs (which must have the same message format) and sends the whole list as a `repeated` field. It is therefore necessary to take into account the size of the message to send due to gRPC/system memory constraints.

This component can also be used with other messages by doing the following:
1. Change the input and output messages in the `.proto` file.
2. Compile the new `.proto` file and copy the resulting files into the `src` folder.
3. Change lines 35 and 36 in `src/main.py` to match the newly created message types in the `.proto` file.

## Usage

The asset can be built with the following command:
```shell
$ docker build .
```
and it can be deployed using the command:
```
$ docker run -p 8061:8061 QUEUE
```
The `-p` flag is used to expose the 8061 docker port according to AI4EU specs.