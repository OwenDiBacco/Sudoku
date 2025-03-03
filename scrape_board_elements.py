from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
Scrapes the sudkou.com webpage using a Webdriver to scrape the content from a board
'''
def find_grid_values_from_sudoku_webpage(grid):
    def initialize_driver():
        chrome_options = Options()
        chrome_options.add_argument("--disable-webgl")  # Disable WebGL to prevent errors
        chrome_options.add_argument("--log-level=3")  # Suppress logs
        chrome_options.add_argument("--disable-logging")  # Suppress unnecessary logs
        chrome_options.add_argument("--headless")  # headless viewing

        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def visit_page_with_driver(url):
        driver.get(url)

    def get_html_content_from_current_page():
        html = driver.page_source
        return BeautifulSoup(html, 'html.parser')
    
    def scrape_webpage_for_table_content():
        frame_elements = soup.find_all("frame")
        for frame_element in frame_elements:
            frame_element_url = frame_element.get("src")
            visit_page_with_driver(frame_element_url)
            frame_url_page_soup = get_html_content_from_current_page()
            puzzle_grid = frame_url_page_soup.find('table', {'id': 'puzzle_grid'})

            if puzzle_grid:
                rows = puzzle_grid.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    row_values = [input_elem.get("value", "") for input_elem in [cell.find("input") for cell in cells] if input_elem]
                    grid.append(row_values)
               
    driver = initialize_driver()

    visit_page_with_driver('https://www.websudoku.com/')
    soup = get_html_content_from_current_page()
    grid = scrape_webpage_for_table_content()
    
    driver.quit()
    return grid