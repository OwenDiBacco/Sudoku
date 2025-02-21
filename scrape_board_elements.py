import time
import turtle
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def loading_icon():
    global stop
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Loading Icon")

    spinner = turtle.Turtle()
    spinner.hideturtle()
    spinner.speed(0)

    stop = False

    def draw_spinner():
        while not stop:
            spinner.clear()
            for i in range(8):
                spinner.penup()
                spinner.goto(0, 0)
                spinner.setheading(i * 45)
                spinner.forward(50)
                spinner.pendown()
                spinner.dot(10, "blue")
                spinner.penup()
                spinner.backward(50)
            spinner.left(10)
            time.sleep(0.1)
        screen.bye()

    draw_spinner()


def find_grid_values_from_sudoku_webpage():
    global stop
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
        
    driver = initialize_driver()

    loading_thread = threading.Thread(target=loading_icon)
    loading_thread.start()

    visit_page_with_driver('https://www.websudoku.com/')
    soup = get_html_content_from_current_page()

    frame_elements = soup.find_all("frame")
    for frame_element in frame_elements:
        frame_element_url = frame_element.get("src")
        visit_page_with_driver(frame_element_url)
        frame_url_page_soup = get_html_content_from_current_page()
        puzzle_grid = frame_url_page_soup.find('table', {'id': 'puzzle_grid'})

        if puzzle_grid:
            rows = puzzle_grid.find_all("tr")
            grid = []
            for row in rows:
                cells = row.find_all("td")
                row_values = [input_elem.get("value", "") for input_elem in [cell.find("input") for cell in cells] if input_elem]

                grid.append(row_values)

            stop = True

            loading_thread.join()
            return grid
        
    driver.quit()