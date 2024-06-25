# FMD-GT

## Usage Instructions

`BRD_runnable.py` is used to generate final strategy distributions by applying e-BRD. There are 3 running modes that were used for the final testing (6(threshold), 7(sorting), 8(random)).

`data_read.py` is used to analyze the results, generating various plots using `GT_charts.py`. Mainly, the last 4 examining modes are used.

Be aware that the main script uses all available CPU cores when running. Due to the way run data is structured (instances of User's referencing each other in the neighbor property), there may be problems with the pickle serializing function in `GT_running_modes.py`, possibly due to undocumented changes in Python.

The file `run_results.zip` contains every run result with the data used in the paper.

## Usage Examples

Here are some usage examples for `BRD_runnable.py`:

- `BRD_runnable.py -f CollegeMsg.txt -m 8 -hv 0 -so -i 10 -l`
- `BRD_runnable.py -f CollegeMsg.txt -m 6 -hv 0`
- `BRD_runnable.py -f CollegeMsg.txt -m 6 -hv 0 -so`
- `BRD_runnable.py -f CollegeMsg.txt -m 6 -hv 0 -a 1.0`

Feel free to modify the command-line arguments as needed for your specific use case.



