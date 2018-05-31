# Samples2PWL

Converts list of samples (originally from DSO8060 oscilloscope output) to PWL file suitable for LTSpice or simillar.

## Usage
`python samples2pwl.py <samples file 1> <samples file 2> <samples file 3> ...`

For each file pointed by argument produces `<original name without extension>.pwl.txt` file.

## Samples (input) file syntax
Text file, any line ending, read line by line. Empty lines are discarded.
Consists of header lines (starting with #) and data lines (not starting with #).

Only one header - `CLOCK` is required.
Syntax: `#CLOCK=<clock period decimal>S`
Specifies period between consequent samples.

All data lines are treated chronologically as samples in Volts stored in decimal form.

See example section for details.

## PWL (output) file syntax
Text file, CLRF.
Each line describes single sample in two columns (separated by tab): time point and value, both stored in decimal form.
Samples are stored chronologically.

See example section for details.

## Example:
Samples (input) file `0-0-0-10k-1000000-1u-ch1.txt`:
```
#CHANNEL:CH1
#CLOCK=0.000001000S
#SIZE=1200
#UNITS:V

4.558636
5.123342
5.374323
5.468440
5.437068
5.468440
5.593930
5.593930
5.562558
5.531185
5.531185
5.531185
5.499813
5.531185
5.562558
(more samples, 1200 total)
```
Command: `python samples2pwl.py 0-0-0-10k-1000000-1u-ch1.txt`
PWL (output) file: `0-0-0-10k-1000000-1u-ch1.pwl.txt`:
```
0.000000        4.558636
0.000001        5.123342
0.000002        5.374323
0.000003        5.46844
0.000004        5.437068
0.000005        5.46844
0.000006        5.59393
0.000007        5.59393
0.000008        5.562558
0.000009        5.531185
0.000010        5.531185
0.000011        5.531185
0.000012        5.499813
0.000013        5.531185
0.000014        5.562558
(more samples, 1200 total)
```