import argparse
import json

def process_metadata(metadata_path):
    biosamples = []

    with open(metadata_path, 'r') as metadata_file:
        next(metadata_file)  # Skip the header
        for line in metadata_file:
            row = line.strip().split('\t')
            if len(row) >= 8:
                biosample_info = {
                    'id': row[0].strip(),
                    'individualId': row[0].strip(),
                    'sex': row[1].strip(),
                    'description': row[8].strip(),
                    'procedure': {
                        'code': {
                            'id': row[2].strip() if len(row) >= 4 else ''
                        }
                    },
                    'files': [{
                        'individualToFileIdentifiers': {
                            'id': row[0].strip() if len(row) >= 3 else ''
                        },
                        'fileAttributes': {
                            'htsFormat': 'VCF',
                            'genomeAssembly': 'GRCh38'
                        }
                    }]
                }
                biosamples.append(biosample_info)

    return biosamples

def generate_json(biosamples, output_path):
    with open(output_path, 'w') as output_file:
        json.dump(biosamples, output_file, indent=4)

def tsv_to_phenopacket(args=None):
    parser = argparse.ArgumentParser(description="Convert TSV metadata to Phenopacket JSON")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input TSV metadata file name")
    parser.add_argument("-o", "--output", type=str, default="phenopacket.json", help="Output Phenopacket JSON file name (default: phenopacket.json)")
    args = parser.parse_args()
    
    
    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)
    
    biosamples = process_metadata(args.input)
    generate_json(biosamples, args.output)

if __name__ == "__main__":
    tsv_to_phenopacket(args.input, args.output)
