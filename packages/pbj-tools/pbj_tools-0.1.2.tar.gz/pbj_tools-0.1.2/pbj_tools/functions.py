import os
import sys
import argparse
import sqlite3
from Bio import SeqIO
import pandas as pd

#
#
### HOMEKEEPING
#
#

def version():
    version = "pbj_tools version 0.1.2"
    print(version)

def valid_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.isdir(dir_path):
        raise argparse.ArgumentTypeError(
            f"{dir_path} is not a valid directory path")
    if not os.access(dir_path, os.R_OK):
        raise argparse.ArgumentTypeError(
            f"{dir_path} is not a readable directory")
    return dir_path

def valid_file(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(
            f"{file_path} is not a valid file path")
    if not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError(
            f"{file_path} is not a readable file")
    return file_path

#
#
### WORKING
#
#

def genbank_to_fasta(input_file, output_file):
    with open(output_file, "w") as fasta_file:
        for record in SeqIO.parse(input_file, "genbank"):
            SeqIO.write(record, fasta_file, "fasta")

def genbank_to_faa(input_file, output_file):
    with open(output_file, "w") as fasta_file:
        for record in SeqIO.parse(input_file, "genbank"):
            SeqIO.write(record, fasta_file, "fasta")

def export_gbk_files(cursor, out):
    cursor.execute("SELECT id, filename, data FROM gbk_data")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            gbk_id, filename, data = row
            file_path = os.path.join(out, filename)
            
            with open(file_path, "wb") as file:
                file.write(data)
            
            print(f"GenBank file '{filename}' exported to '{file_path}' successfully.")
    else:
        print("No GenBank files found in the database.")

def show_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    for table in table_names:
        print(table)

def export_tables(connection, cursor, out):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    for table in table_names:
        df = pd.read_sql_query(f"SELECT * FROM {table[0]}", connection)
        outfile = os.path.join(out, f"{table[0]}.csv")

        if os.path.exists(outfile):
            print(f"{table[0]} \t exists already, moving on...")
            continue
        else:
            df.to_csv(outfile, index=False)
            print(f"{table[0]} \t export to csv file")
            