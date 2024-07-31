import argparse
import json
import os
import sys

def xyz_to_json(xyz_file, basis_set, aux_basis_set, driver, method):
    with open(xyz_file, 'r') as f:
        lines = f.readlines()
    
    num_atoms = int(lines[0].strip())
    symbols = []
    geometry = []
    
    for line in lines[2:2 + num_atoms]:
        parts = line.split()
        symbols.append(parts[0])
        geometry.extend(map(float, parts[1:4]))

    if method == "RestrictedRIMP2" and not aux_basis_set:
        aux_basis_set = "cc-pVDZ-RIFIT"

    model_data = {
        "method": method,
        "basis": basis_set
    }


    if aux_basis_set:
        model_data["aux_basis"] = aux_basis_set

    keywords_data = {
        "scf": {
            "max_iters": 100,
            "max_diis_history_length": 8,
            "batch_size": 2560,
            "convergence_metric": "Energy",
            "convergence_threshold": 1e-5,
            "use_ri": False
        }
    }
    if driver == "Optimization":
        keywords_data["optimization"] = {
            "max_iters": 30
        }
    if driver == "Dynamics":
        keywords_data["dynamics"] = {
            "dt": 0.001,
            "n_timesteps": 10
        }

    data = {
        "topologies": [
            {
                "fragment_formal_charges": [0],
                "geometry": geometry,
                "symbols": symbols
            }
        ],
        "model": model_data,
        "system": {
            "max_gpu_memory_mb": 4000
        },
        "keywords": keywords_data,
        "driver": driver
    }


    return json.dumps(data, indent=2)

def json_to_xyz(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    topology = data['topologies'][0]
    symbols = topology['symbols']
    geometry = topology['geometry']
    
    num_atoms = len(symbols)
    lines = [f"{num_atoms}", "",]
    
    for i in range(num_atoms):
        symbol = symbols[i]
        x, y, z = geometry[3*i:3*i+3]
        lines.append(f"{symbol} {x:.6f} {y:.6f} {z:.6f}")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Convert between XYZ and JSON formats.')
    parser.add_argument('--input_format', choices=['xyz', 'json'], help='Input file format (default: xyz)')
    parser.add_argument('--output_format', choices=['json', 'xyz'], help='Output file format (default: json)')
    parser.add_argument('--input_file', required=True, help='Input file name')
    parser.add_argument('--output_file', help='Output file name (default: input_file with appropriate suffix)')
    parser.add_argument('--basis_set', default='6-31G', help='Basis set to use (default: 6-31G)')
    parser.add_argument('--aux_basis_set', default='', help='Auxiliary basis set (default: none)')
    parser.add_argument('--driver', default='Energy', help='Driver to use (default: Energy) (options: Energy, Gradient, Dynamics, Optimization)')
    parser.add_argument('--method', default='RestrictedHF', help='Method to use (default: RestrictedHF) (options: RestrictedHF and RestrictedRIMP2)')
    
    args = parser.parse_args()

    input_format = args.input_format if args.input_format else 'xyz'
    output_format = args.output_format if args.output_format else 'json'
    
    if not args.output_file:
        input_file_base, input_file_ext = os.path.splitext(args.input_file)
        output_file_ext = 'json' if output_format == 'json' else 'xyz'
        output_file = f"{input_file_base}.{output_file_ext}"
    else:
        output_file = args.output_file
    
    if input_format == 'xyz' and output_format == 'json':
        output_data = xyz_to_json(args.input_file, args.basis_set, args.aux_basis_set, args.driver, args.method)
    elif input_format == 'json' and output_format == 'xyz':
        output_data = json_to_xyz(args.input_file)
    else:
        print("Unsupported conversion.", file=sys.stderr)
        sys.exit(1)
    
    with open(output_file, 'w') as f:
        f.write(output_data)

if __name__ == '__main__':
    main()

