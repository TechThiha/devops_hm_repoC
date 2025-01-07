import argparse
import csv
import re
from pathlib import Path

def parse_doxygen_warning(line):
    """Parse a single line of Doxygen warning log."""
    # Common Doxygen warning pattern:
    # /path/to/file:line: warning: message
    pattern = r"^(.*):(\d+):\s*warning:\s*(.*)$"
    match = re.match(pattern, line.strip())
    
    if match:
        return {
            'file': match.group(1),
            'line': match.group(2),
            'message': match.group(3)
        }
    return None

def process_warnings_file(input_file, output_file):
    """Process the Doxygen warnings file and output to CSV."""
    warnings = []
    
    with open(input_file, 'r') as f:
        for line in f:
            result = parse_doxygen_warning(line)
            if result:
                warnings.append(result)
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'line', 'message'])
        writer.writeheader()
        writer.writerows(warnings)
    
    return len(warnings)

def main():
    parser = argparse.ArgumentParser(description='Parse Doxygen warning logs to CSV')
    parser.add_argument('input_file', type=str, help='Path to the Doxygen warnings log file')
    parser.add_argument('--output', type=str, default='doxygen_warnings.csv',
                      help='Output CSV file path (default: doxygen_warnings.csv)')
    
    args = parser.parse_args()
    
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' does not exist")
        return 1
    
    try:
        warning_count = process_warnings_file(args.input_file, args.output)
        print(f"Successfully processed {warning_count} warnings to {args.output}")
        return 0
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1

if __name__ == "__main__":
    exit(main())