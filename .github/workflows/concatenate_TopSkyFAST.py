import os

def concatenate_files(source_directory, shared_directory, output_file, allowed_files=None):
    sources = []

    if os.path.isdir(shared_directory):
        for filename in sorted(os.listdir(shared_directory)):
            fp = os.path.join(shared_directory, filename)
            if os.path.isfile(fp):
                if allowed_files is None or filename in allowed_files:
                    sources.append(fp)

    if os.path.isdir(source_directory):
        for filename in sorted(os.listdir(source_directory)):
            fp = os.path.join(source_directory, filename)
            if os.path.isfile(fp):
                sources.append(fp)

    with open(output_file, 'w') as outfile:
        for file_path in sources:
            with open(file_path, 'r') as infile:
                for line in infile:
                    stripped_line = line.strip()
                    if stripped_line:
                        if stripped_line.startswith('//&preserve'):
                            stripped_line = '//' + stripped_line[len('//&preserve'):].strip()
                        elif stripped_line.startswith('//'):
                            continue
                        outfile.write(stripped_line + '\n')

def main():
    base_dir = '.data/TopSkyFAST'
    shared_dir = os.path.join(base_dir, '_shared')
    targets = [
        ('CTA',           'OMAE/Plugins/TopSky/TopSky CTA/TopSkyFAST.txt',           None),
        ('CTA Abu Dhabi', 'OMAE/Plugins/TopSky/TopSky CTA Abu Dhabi/TopSkyFAST.txt', ['OMAA.txt']),
        ('CTA Dubai',     'OMAE/Plugins/TopSky/TopSky CTA Dubai/TopSkyFAST.txt',      ['OMDB.txt', 'OMDW.txt', 'OMSJ.txt']),
        ('Enroute',       'OMAE/Plugins/TopSky/TopSky Enroute/TopSkyFAST.txt',        None),
    ]

    for source_subdir, target_file, allowed_files in targets:
        source_directory = os.path.join(base_dir, source_subdir)
        print(f'Building {target_file}')
        concatenate_files(source_directory, shared_dir, target_file, allowed_files)
        print(f'{target_file} built successfully.')

if __name__ == '__main__':
    main()