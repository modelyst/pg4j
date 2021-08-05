'''
Usage:
    import.py [options]

Options:
    --data-dir ARG            Path to the folder that contains nodes and edges subfolders [default: .]
    --regex ARG               Only import .csv's whose name matches this regex string [default: .*]
    --run                     Run the import.sh script immediately after generating it
    --neo4j-path ARG          Path to where neo4j stores databases [default: /usr/local/var/neo4j/data/]
    --dbname ARG              Name of neo4j database [default: test]
'''

from docopt import docopt
from pathlib import Path
from os import system, listdir
from os.path import join
from re import match

def generate_shell_script(args):
    script = 'neo4j stop\n'
    script += f"rm -rf {join(args['--neo4j-path'], 'databases', args['--dbname'])}\n"
    script += f"rm -rf {join(args['--neo4j-path'], 'transactions', args['--dbname'])}\n"
    script += 'neo4j admin import \\\n'
    script += '    --id-type=STRING \\\n'
    script += '    --skip-duplicate-nodes \\\n'

    subfolders = ['nodes','edges']
    neo4j_types = ['nodes', 'relationships']
    for subfolder, neo4j_type in zip(subfolders, neo4j_types):
        csv_folder = Path(args['--data-dir']) / subfolder
        for fname in listdir(csv_folder):
            [name, extension] = fname.split('.')
            if match(args['--regex'], name) and extension=='csv':
                full_path = csv_folder / fname
                script += f'    --{neo4j_type}={full_path} \\\n'

    script += f"    --database {args['--dbname']}\n"
    script += 'neo4j start'

    return script

def main():
    args = docopt(__doc__)
    # print(args)
    # breakpoint()
    data_dir = Path(args['--data-dir'])
    shell_script = generate_shell_script(args)

    out_fname = data_dir / 'import.sh'
    with open(out_fname,'w') as f:
        f.write(shell_script)

    if args['--run']:
        system(out_fname)


if __name__ == "__main__":
    main()