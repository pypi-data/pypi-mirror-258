# Phage jelly tools 

### Usage:
There are two ways to use the db_tools package:
* Use the command db_tools from bash command line
* Open a python terminal and import the functions

___

Install pbj_tools
```sh
pip install pbj-tools
```

Execute the help script:
```sh
pbj_tools --help
```

Extract genomes from the database into an output directory (nucleotide fasta format):
```bash
pbj_tools -db phage.db --output <genomes_dir> --export nuc
```

**To use the functions provided within:**
```py
# Import module
import pbj_tools as pb

# Display version
pb.version()

# Display functions available
dir(pb)
```

**Connect and interact with database**
```py
import pbj_tools as pb
connection, cursor = pb.connect('./phage.db')

# Show tables within database
pb.show_tables(cursor)

# Read one of the tables into a dataframe
df = pb.read_table(connection, 'TABLE')

```