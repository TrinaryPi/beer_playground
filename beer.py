from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup
import pandas as pd
import sys
import pathlib
import json

    # column_headers = None
    # # find the hyperlinks of all recipes on the page
    #
    #
    #         recipe_html = urlopen()
    #         soup = BeautifulSoup(recipe_html, 'lxml')
    #         recipe_table = soup.find('table', {'class': 'r_hdr'})
    #         if column_headers is None:
    #             column_headers = [th.getText() for th in
    #                               recipe_table.findAll('th' and 'b')]
    #             print(column_headers)


def read_in_recipe_list(directory):
    """get previous list of recipes and links"""
    file_name = "recipes.json"
    recipe_list_file = pathlib.Path(directory) / file_name
    recipe_dict = {}
    if recipe_list_file.exists():
        with open(recipe_list_file, 'r') as f:
            recipe_dict = json.loads(f.read())
    else:
        with open(recipe_list_file, 'w+') as f:
            f.write(json.dumps(recipe_dict))

    return recipe_dict


def get_recipes(base_url, minmax, recipe_dict):
    """get recipes form number of pages"""
    total_count = 0
    for page in range(minmax[0], minmax[1]):
        base_url = base_url[:-1] + "%d" % page
        try:
            bsr_html = urlopen(base_url)
        except URLError as e:
            print("ERROR: An error occured fetching %s. \n %s."
                  % (base_url, e.reason))
            return 0
        soup = BeautifulSoup(bsr_html, 'lxml')
        # parse soup for recipe names and links on page
        count = parse_recipe_links(soup, recipe_dict)
        total_count += count
        if count == 0:
            print("No new recipes were found on %s." % base_url)

    return total_count


def parse_recipe_links(soup, recipe_dict):
    """get all recipe hyperlinks from page"""
    # recipe links found in h4 object
    count = 0
    for h4 in soup.find_all('h4'):
        # find all 'a' tagged objects in h4 object
        for recipe in h4.find_all('a'):
            # if recipe.string not in recipe_dict:
            name = str(recipe.string)
            recipe_dict[name] = recipe.get('href')
            count += 1

    return count


def write_recipe_list(directory, recipe_dict):
    """write new recipes and links to file"""
    file_name = "recipes.json"
    recipe_list_file = pathlib.Path(directory) / file_name

    with open(recipe_list_file, 'w+') as f:
        f.write(json.dumps(recipe_dict, indent=4, separators=(',', ': '),
                           ensure_ascii=False))


def main():
    bsr_url = "https://beersmithrecipes.com/toprated/0"  # page 1
    minmax_pages = [0, 11]
    output_dir = "./raw_recipes/"

    recipe_dict = read_in_recipe_list(output_dir)
    new_recipes = get_recipes(bsr_url, minmax_pages, recipe_dict)
    if new_recipes > 0:
        write_recipe_list(output_dir, recipe_dict)

    if len(recipe_dict) == 0:
        print("No recipes found. Exiting.")
        sys.exit()


if __name__ == '__main__':
    status = main()
    sys.exit(status)
