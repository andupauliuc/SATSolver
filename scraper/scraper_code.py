import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
from time import sleep

params = {
    'p_link':'http://www.menneske.no/sudoku/5/eng/',
    'p_sol':'http://www.menneske.no/sudoku/5/eng/solution.html?number={}',
}
counter = 5000
i = 1

df = pd.DataFrame({'puzzle':[], 'solutions':[]})
df.to_csv('sudoku_5.csv', index=False, sep=',')


def get_sudokus(p):
    puzzle_link = p['p_link']
    solution_link = p['p_sol']

    req = requests.get(puzzle_link)
    c = req.content
    soup = BeautifulSoup(c, 'html.parser')

    grid_txt = soup.find_all('div', {'class':'grid'})[0].text
    puzzle_no = grid_txt[str.find(grid_txt, 'Showing puzzle')+23:str.find(grid_txt, 'Puzzletype')]

    rows = soup.find_all('tr', {'class':'grid'})
    puzzle = []
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            if txt != '\xa0':
                puzzle.append(txt)
            else:
                puzzle.append('0')
    puzzle = ' '.join(puzzle)


    req_sol = requests.get(solution_link.format(puzzle_no))
    c = req_sol.content
    soup = BeautifulSoup(c, 'html.parser')
    rows = soup.find_all('tr', {'class':'grid'})
    solution = []
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            if txt != '\xa0':
                solution.append(txt)
            else:
                solution.append('0')
    solution = ' '.join(solution)

    return puzzle, solution


def tryAgain(retries=0):
    if retries > 50: return
    try:
        with open('sudoku_5.csv', 'a') as f:
            writer = csv.writer(f)
            global i

            while i <= counter:
                puzzle_no_list = []

                p, s = get_sudokus(params)

                writer.writerow([p, s])
                f.flush()

                i += 1

    except Exception as e:
        print(e)
        sleep(2)
        retries+=1
        tryAgain(retries)


tryAgain(0)
