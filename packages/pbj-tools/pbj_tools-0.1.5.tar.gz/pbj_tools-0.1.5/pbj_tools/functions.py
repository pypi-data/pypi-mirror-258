import os
import sys
import argparse
import sqlite3
from Bio import SeqIO
import pandas as pd

###
# CLASSES

class Reads(object):
    '''
    For read pairs (Normally illumina)
    '''
    def __init__(self, name, info, read_1, read_2):
        self.name = name;
        self.info = info;
        self.read_1 = read_1;
        self.read_2 = read_2;

class Phage(object):
    '''
    For use in holding phage data for export
    '''
    def __init__(self, tag, info):
        self.tag = tag;
        self.info = info;

###

#
#
### HOMEKEEPING
#
#

def version():
    version = "pbj_tools version 0.1.5"
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

# FAULTY
'''
def genbank_to_faa(input_file, output_file):
    with open(output_file, "w") as fasta_file:
        for record in SeqIO.parse(input_file, "genbank"):
            SeqIO.write(record.translate(), fasta_file, "fasta")
'''

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

#
#
### API specific
#
#

def connect(database):
    if os.path.exists(database):
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        return connection, cursor
    else:
        print("Error, path invalid")

def read_table(connection, table):
    df = pd.read_sql_query(f"SELECT * FROM {table}", connection)
    return df

def find_read_pairs(input_dir, description, r1_ext, r2_ext):
    '''
    Returns read pairs within an input directory
    '''
    if not description:
        description = 'Unknown pair'
    read_pairs = []
    for file in os.listdir(input_dir):
        filepath_1 = os.path.join(input_dir, file)
        if file.endswith(r1_ext):
            cut = len(r1_ext)
            name = file[:-cut]
            filepath_2 = os.path.join(input_dir, name + r2_ext)
            if os.path.isfile(filepath_2):
                print("Input file", f"Adding pair: {name}")
                pair = Reads(name, filepath_1, filepath_2)
                read_pairs.append(pair)
            else:
                print("Input file", f"No second read file found for: {name}")
    print("Pairing input files", f"Read pairs = {len(read_pairs)}")
    return read_pairs

def export_phage_data(tag):
    '''
    Extract data pertaining to a single phage
    Returns a single Phage object
    '''
    pass

def export_phage_list(tag):
    '''
    Extract all data pertaining to phages within a list
    Returns a list of Phage objects
    '''
    pass

def import_gbk(connection, cursor, gbk, commit=False):
    with open(gbk, "rb") as file:
        data = file.read()
    filename = os.path.basename(gbk)
    cursor.execute("INSERT INTO gbk_data (filename, data) VALUES (?, ?)", (filename, sqlite3.Binary(data)))
    print(f"GenBank file '{filename}' imported into the database.")
    if commit:
        connection.commit()
        print("Changes have been committed")
    else:
        print("No changes to database made, set commit=True to apply changes")

def reformat_fasta_dir(input_dir):
    '''
    Reformats all fasta files within a directory
    '''
    records = []
    for file in os.listdir(input_dir):
        file = os.path.join(input_dir, file)
        with open(file, "r") as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                records.append(record)
    for file in records:
        file = os.path.join(input_dir, f"{file.id}.fasta")
        with open(file, "w") as fasta_file:
            SeqIO.write(file, fasta_file, "fasta")

def reformat_fasta(input_fasta, output_fasta):
    '''
    Reformats a single fasta file
    '''
    records = []
    with open(input_fasta, "r") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            records.append(record)
    for file in records:
        with open(output_fasta, "w") as fasta_file:
            SeqIO.write(file, fasta_file, "fasta")
