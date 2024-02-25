def main():
    import os
    import sys
    import argparse
    import sqlite3
    from Bio import SeqIO

    # Homekeeping functions
    from .functions import version, valid_dir, valid_file

    # Working functions
    from .functions import export_tables, export_gbk_files
    from .functions import genbank_to_fasta, genbank_to_faa

    # Parsing arguments
    parser = argparse.ArgumentParser(description=f"PBJ (Peanut butter jelly) export tool: https://github.com/JoshuaIszatt")

    # Options
    parser.add_argument('-db', '--database', type=valid_file,
                        help='Database file (.db)')
    parser.add_argument('-e', '--export', choices=['tables', 'nuc','aa','gbk'], 
                        help='Export tables as csv files or genomes as genbank, nucleotide sequences or amino acid sequences',
                        default='tables')
    parser.add_argument('-o', '--output', type=valid_dir, 
                        help='Output directory path', 
                        default=os.path.join(os.getcwd(), 'exports'))
    parser.add_argument('-v', '--version', action="store_true", 
                        help='Print the db_tools version')
    args = parser.parse_args()

    # Printing version
    if args.version:
        sys.exit(version())
    
    # Connect to database if it is given
    if args.database:
        print(f"Database: {args.database}")
        connection = sqlite3.connect(args.database)
        cursor = connection.cursor()
    else:
        sys.exit("No database provided")
    
    # Exporting files
    if args.export == 'tables':
        export_tables(connection, cursor, args.output)
    elif args.export == 'gbk':
        export_gbk_files(cursor, args.output)
    elif args.export == 'nuc':
        export_gbk_files(cursor, args.output)
        for file in os.listdir(args.output):
            if not file.endswith('.gbk'):
                print(f"Skipping {file}")
                continue
            path = os.path.join(args.output, file)
            fa = os.path.join(args.output, file.replace(".gbk", ".fa"))
            genbank_to_fasta(path, fa)
            if os.path.exists(fa):
                print(f"{fa} converted successfully")
                os.remove(path)
    elif args.export == 'aa':

        sys.exit("This feature is still under development")
        
        export_gbk_files(cursor, args.output)
        for file in os.listdir(args.output):
            path = os.path.join(args.output, file)
            fa = os.path.join(args.output, file.replace(".gbk", ".fa"))
            genbank_to_fasta(path, fa)
            if os.path.exists(fa):
                print(f"{fa} converted successfully")
                os.remove(path)


