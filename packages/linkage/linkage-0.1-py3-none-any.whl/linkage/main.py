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
    print(" How to Use \n ")
    print(" This script is to transform the links of the .html file, to the Github repository \n ")
    print("")
    print(" 1) Takes the Github Url to prefix the links \n")
    print("        Use This as default https://github.com/semanticClimate/ipcc/blob/main/cleaned_content/  \n")
    print(" 2) Path to remove from the links for example:\n"
      "        Suppose your file paths in original HTML are like '/home/user/project/outut.html' \n \n"
      "        to remove '/home/user' and retain '/project/output.html', type '/home/user'\n \n"
      "        Use this as default: '/content/pyamihtml/test/resources/ipcc/cleaned_content/'\n \n")

    input_file_namepath = input(" Enter the file path to be transformed: ")
    output_file_namepath = input(" Enter the file path for output: ")
    github_url = input (" Github Repository Url : ")
    print("")
    print(f" We are about to prefix all links in the HTML file to : {github_url}  " )  # Replace 'https://github.com/something/something' with your GitHub URL
    print("")
    path_to_remove = input(" Path to remove from the links for in the local file " )  # Specify the part of the file path to remove
    print("\n"
      f" Removing {path_to_remove} \n"
      f" and then adding {github_url} to all the links \n"
      f" Of the {input_file_namepath} \n"
      f" and making {output_file_namepath} as output file : " )
    print("\n")
    modify_github_links(input_file_namepath, output_file_namepath, github_url, path_to_remove)

    print("\n")
if __name__ == '__main__':
    main()
