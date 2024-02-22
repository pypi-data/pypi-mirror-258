# Compspec IOR

<p align="center">
  <img height="300" src="https://raw.githubusercontent.com/compspec/spec/main/img/compspec-circle.png">
</p>

[![PyPI version](https://badge.fury.io/py/compspec-ior.svg)](https://badge.fury.io/py/compspec-ior)

A compspec (Composition spec) is a specification and model for comparing things. Compspec IOR is
a plugin for extraction of [IOR](https://github.com/hpc/ior) metadata from applications, and packaging in compatibility specification
artifacts. This means that we also maintain the compatibility schema here. To learn more:

 - [Compspec](https://github.com/compspec/compspec): the Python library that discovers and loads this plugin.
 - [Compatibility](https://github.com/compspec/spec/tree/main/compatibility): of container images and applications to a host environment.
 - [Compspec Go](https://github.com/compspec/compspec-go): the Go library that retrieves artifacts and makes graphs for image selection and scheduling.


## Usage

Install compspec and the plugin here:

```bash
pip install compspec
pip install compspec-ior
```

Then run an extraction with IOR. You can use defaults, or add any parameters to IOR after the plugin name "ior"
Here is how to print to the terminal:

```bash
compspec extract ior
```

<details>

<summary>IOR output</summary>

```console
{
    "version": "0.0.0",
    "kind": "CompatibilitySpec",
    "metadata": {
        "name": "compat-experiment",
        "schemas": {
            "io.compspec.ior": "https://raw.githubusercontent.com/compspec/compspec-ior/main/compspec_ior/schema.json"
        }
    },
    "compatibilities": [
        {
            "name": "io.compspec.ior",
            "version": "0.0.0",
            "attributes": {
                "version": "4.0.0rc1",
                "began": "Thu Feb 22 00:36:12 2024",
                "machine": "Linux 2b3ee0c4c948",
                "finished": "Thu Feb 22 00:36:12 2024",
                "command_line": "ior -O summaryFormat=JSON",
                "summary.write.operation": "write",
                "summary.write.API": "POSIX",
                "summary.write.TestID": 0,
                "summary.write.ReferenceNumber": 0,
                "summary.write.segmentCount": 1,
                "summary.write.blockSize": 1048576,
                "summary.write.transferSize": 262144,
                "summary.write.numTasks": 1,
                "summary.write.tasksPerNode": 1,
                "summary.write.repetitions": 1,
                "summary.write.filePerProc": 0,
                "summary.write.reorderTasks": 0,
                "summary.write.taskPerNodeOffset": 1,
                "summary.write.reorderTasksRandom": 0,
                "summary.write.reorderTasksRandomSeed": 0,
                "summary.write.bwMaxMIB": 904.92,
                "summary.write.bwMinMIB": 904.92,
                "summary.write.bwMeanMIB": 904.92,
                "summary.write.bwStdMIB": 0.0,
                "summary.write.OPsMax": 3619.6798,
                "summary.write.OPsMin": 3619.6798,
                "summary.write.OPsMean": 3619.6798,
                "summary.write.OPsSD": 0.0,
                "summary.write.MeanTime": 0.0011,
                "summary.write.xsizeMiB": 1.0,
                "summary.read.operation": "read",
                "summary.read.API": "POSIX",
                "summary.read.TestID": 0,
                "summary.read.ReferenceNumber": 0,
                "summary.read.segmentCount": 1,
                "summary.read.blockSize": 1048576,
                "summary.read.transferSize": 262144,
                "summary.read.numTasks": 1,
                "summary.read.tasksPerNode": 1,
                "summary.read.repetitions": 1,
                "summary.read.filePerProc": 0,
                "summary.read.reorderTasks": 0,
                "summary.read.taskPerNodeOffset": 1,
                "summary.read.reorderTasksRandom": 0,
                "summary.read.reorderTasksRandomSeed": 0,
                "summary.read.bwMaxMIB": 6615.6215,
                "summary.read.bwMinMIB": 6615.6215,
                "summary.read.bwMeanMIB": 6615.6215,
                "summary.read.bwStdMIB": 0.0,
                "summary.read.OPsMax": 26462.4858,
                "summary.read.OPsMin": 26462.4858,
                "summary.read.OPsMean": 26462.4858,
                "summary.read.OPsSD": 0.0,
                "summary.read.MeanTime": 0.0002,
                "summary.read.xsizeMiB": 1.0,
                "test.0.starttime": "Thu Feb 22 00:36:12 2024",
                "test.0.capacity": "1.8 TiB",
                "test.0.used_capacity": "20.2%",
                "test.0.inodes": "116.4 Mi",
                "test.0.used_inodes": "5.3%",
                "test.0.parameters.testID": 0,
                "test.0.parameters.refnum": 0,
                "test.0.parameters.api": "POSIX",
                "test.0.parameters.platform": "2b3ee0c4c(Linux)",
                "test.0.parameters.testFileName": "testFile",
                "test.0.parameters.deadlineForStonewall": 0,
                "test.0.parameters.stoneWallingWearOut": 0,
                "test.0.parameters.maxTimeDuration": 0,
                "test.0.parameters.outlierThreshold": 0,
                "test.0.parameters.options": "(null)",
                "test.0.parameters.dryRun": 0,
                "test.0.parameters.nodes": 1,
                "test.0.parameters.memoryPerTask": 0,
                "test.0.parameters.memoryPerNode": 0,
                "test.0.parameters.tasksPerNode": 1,
                "test.0.parameters.repetitions": 1,
                "test.0.parameters.multiFile": 0,
                "test.0.parameters.interTestDelay": 0,
                "test.0.parameters.fsync": 0,
                "test.0.parameters.fsyncperwrite": 0,
                "test.0.parameters.useExistingTestFile": 0,
                "test.0.parameters.uniqueDir": 0,
                "test.0.parameters.singleXferAttempt": 0,
                "test.0.parameters.readFile": 1,
                "test.0.parameters.writeFile": 1,
                "test.0.parameters.filePerProc": 0,
                "test.0.parameters.reorderTasks": 0,
                "test.0.parameters.reorderTasksRandom": 0,
                "test.0.parameters.reorderTasksRandomSeed": 0,
                "test.0.parameters.randomOffset": 0,
                "test.0.parameters.checkWrite": 0,
                "test.0.parameters.checkRead": 0,
                "test.0.parameters.dataPacketType": 0,
                "test.0.parameters.keepFile": 0,
                "test.0.parameters.keepFileWithError": 0,
                "test.0.parameters.warningAsErrors": 0,
                "test.0.parameters.verbose": 0,
                "test.0.parameters.data packet type": "g",
                "test.0.parameters.setTimeStampSignature/incompressibleSeed": 0,
                "test.0.parameters.collective": 0,
                "test.0.parameters.segmentCount": 1,
                "test.0.parameters.transferSize": 262144,
                "test.0.parameters.blockSize": 1048576,
                "test.0.options.api": "POSIX",
                "test.0.options.apiVersion": "",
                "test.0.options.test filename": "testFile",
                "test.0.options.access": "single-shared-file",
                "test.0.options.type": "independent",
                "test.0.options.segments": 1,
                "test.0.options.ordering in a file": "sequential",
                "test.0.options.ordering inter file": "no tasks offsets",
                "test.0.options.nodes": 1,
                "test.0.options.tasks": 1,
                "test.0.options.clients per node": 1,
                "test.0.options.repetitions": 1,
                "test.0.options.xfersize": "262144 bytes",
                "test.0.options.blocksize": "1 MiB",
                "test.0.options.aggregate filesize": "1 MiB",
                "test.0.results.0.access": "write",
                "test.0.results.0.bwMiB": 904.92,
                "test.0.results.0.blockKiB": 1024.0,
                "test.0.results.0.xferKiB": 256.0,
                "test.0.results.0.iops": 3842.6972,
                "test.0.results.0.latency": 0.0003,
                "test.0.results.0.openTime": 0.0001,
                "test.0.results.0.wrRdTime": 0.001,
                "test.0.results.0.closeTime": 0.0,
                "test.0.results.0.totalTime": 0.0011,
                "test.0.results.1.access": "read",
                "test.0.results.1.bwMiB": 6615.6215,
                "test.0.results.1.blockKiB": 1024.0,
                "test.0.results.1.xferKiB": 256.0,
                "test.0.results.1.iops": 27962.0267,
                "test.0.results.1.latency": 0.0,
                "test.0.results.1.openTime": 0.0,
                "test.0.results.1.wrRdTime": 0.0001,
                "test.0.results.1.closeTime": 0.0,
                "test.0.results.1.totalTime": 0.0002
            }
        }
    ]
}
```

</details>

And how to save to file

```bash
compspec  extract --outfile ior-test.json ior
```

And run the example to see how to use compspec-ior directly in Python to generate the same
artifact.

```bash
python ./examples/singleton-run.py
```


### Development

If you open the [Development container](.devcontainer) in VSCode, you'll find ior on the path:

```bash
$ which ior
/usr/bin/ior
```

This allows us to easily develop and test the compatibility plugin. You can

## TODO

- how to handle adding lists (with indices) to schema?

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
