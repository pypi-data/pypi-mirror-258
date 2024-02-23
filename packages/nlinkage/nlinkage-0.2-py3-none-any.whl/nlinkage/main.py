from bs4 import BeautifulSoup

def modify_github_links(input_file, output_file, github_url, path_to_remove):
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all anchor tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Split the file path and remove the specified part
        split_path = href.split(path_to_remove)[-1]
        # Modify the href attribute based on the specified GitHub URL
        modified_href = f'{github_url}{split_path}'
        a_tag['href'] = f'https://htmlpreview.github.io/?{modified_href}'

    # Write the modified HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():

    input_file_namepath = '/content/pyamihtml/output/result.html'
    output_file_namepath = '/content/pyamihtml/output/result.html'
    github_url = 'https://github.com/ydv-amit-ydv/ipcc/blob/main/cleaned_content/' #https://github.com/flower1430/semantic_Climate/tree/main/cleaned_content
    print(f" We are about to prefix all links in the HTML file to : {github_url}  " )
    path_to_remove = '/content/pyamihtml/test/resources/ipcc/cleaned_content/'
    print("\n"
      f" Removing {path_to_remove} \n"
      f" and then prefixing {github_url} to all the links \n"
      f" and overwriting {input_file_namepath} \n"
      f" to make a final output {output_file_namepath} as output file : " )
    print("\n")
    print(f" After the execution of this script download the {output_file_namepath} , and open it get results \n")
    print("\n")
    modify_github_links(input_file_namepath, output_file_namepath, github_url, path_to_remove)

    print("\n")
if __name__ == '__main__':
    main()
