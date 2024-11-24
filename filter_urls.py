file_path = 'broken_urls.py'
urls = []
url_pattern = r'https?://[^\s,]+'

url_accumulator = ""

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('http'):
            if url_accumulator:
                urls.append(url_accumulator)
            url_accumulator = line
        else:
            url_accumulator += line

    if url_accumulator:
        urls.append(url_accumulator)

with open('urls.py', 'w') as output_file:
    output_file.write('urls = [\n')
    for url in urls:
        output_file.write(f'    "{url}",\n')
    output_file.write(']')
