# parley_exess

A simple python script that will transform xyz to exess json input format and viceversa

```
usage: parley.py [-h] [--input_format {xyz,json}] [--output_format {json,xyz}] --input_file INPUT_FILE [--output_file OUTPUT_FILE]
                 [--basis_set BASIS_SET] [--aux_basis_set AUX_BASIS_SET] [--driver DRIVER] [--method METHOD]

Convert between XYZ and JSON formats.

optional arguments:
  -h, --help            show this help message and exit
  --input_format {xyz,json}
                        Input file format (default: xyz)
  --output_format {json,xyz}
                        Output file format (default: json)
  --input_file INPUT_FILE
                        Input file name
  --output_file OUTPUT_FILE
                        Output file name (default: input_file with appropriate suffix)
  --basis_set BASIS_SET
                        Basis set to use (default: 6-31G)
  --aux_basis_set AUX_BASIS_SET
                        Auxiliary basis set (default: none)
  --driver DRIVER       Driver to use (default: Energy) (options: Energy, Gradient, Dynamics, Optimization)
  --method METHOD       Method to use (default: RestrictedHF) (options: RestrictedHF and RestrictedRIMP2)
```
