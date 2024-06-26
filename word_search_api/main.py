from fastapi import FastAPI, Query
import random
import string
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed


description = """
The Word Search Puzzle API is a FastAPI application that generates customizable word search puzzles. This API supports creating puzzles with words placed horizontally, vertically, diagonally, and in reverse. 

Users can specify the words to be included and optionally set a minimum grid size. 

The generated puzzles are returned in JSON format, making it easy to integrate into various applications.
"""

tags_metadata = [
    {
        "name": "WordSearchPuzzles",
        "description": "Endpoints for generating and retrieving word search puzzles.",
    }
]

app = FastAPI(title= "Word Search Puzzle API",description=description,openapi_tags = tags_metadata)

def create_grid(size):
    return np.full((size, size), ' ')

def place_word(grid, word, row, col, direction):
    size = len(grid)
    if direction == 'H' and col + len(word) <= size:
        if all(grid[row, col + i] in (' ', word[i]) for i in range(len(word))):
            for i in range(len(word)):
                grid[row, col + i] = word[i]
            return True
    elif direction == 'V' and row + len(word) <= size:
        if all(grid[row + i, col] in (' ', word[i]) for i in range(len(word))):
            for i in range(len(word)):
                grid[row + i, col] = word[i]
            return True
    elif direction == 'D' and row + len(word) <= size and col + len(word) <= size:
        if all(grid[row + i, col + i] in (' ', word[i]) for i in range(len(word))):
            for i in range(len(word)):
                grid[row + i, col + i] = word[i]
            return True
    elif direction == 'B' and col - len(word) >= -1 and row - len(word) >= -1:
        if all(grid[row - i, col - i] in (' ', word[i]) for i in range(len(word))):
            for i in range(len(word)):
                grid[row - i, col - i] = word[i]
            return True
    return False

def fill_empty_spaces(grid):
    letters = string.ascii_uppercase
    empty_positions = np.where(grid == ' ')
    for pos in zip(*empty_positions):
        grid[pos] = random.choice(letters)

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def calculate_min_size(words):
    max_word_length = max(len(word) for word in words)
    total_chars = sum(len(word) for word in words)
    return max(max_word_length, int(total_chars ** 0.5) + 1)

def try_place_word(grid, word):
    directions = ['H', 'V', 'D', 'B']  # Added 'B' for backward diagonal
    for _ in range(100):  # Limit the number of attempts to place each word
        direction = random.choice(directions)
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid) - 1)
        if place_word(grid, word, row, col, direction):
            return True
    return False

def try_place_all_words(grid, words):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(try_place_word, grid, word) for word in words]
        for future in as_completed(futures):
            if not future.result():
                return False
    return True

def generate_word_search(words, min_size=0):
    if min_size == 0:
        size = calculate_min_size(words)
    else:
        size = max(min_size, calculate_min_size(words))
    
    grid = create_grid(size)

    while not try_place_all_words(grid, words):
        size += 1
        grid = create_grid(size)
    
    fill_empty_spaces(grid)
    return grid

# FastAPI endpoints

@app.get("/word-search/",tags= ["WordSearchPuzzles"])
async def get_word_search_puzzle(
    words: str = Query(..., description="Comma-separated list of words to include in the puzzle"),
    min_size: int = Query(0, description="Minimum size of the grid (optional)")
):

    words_list = [word.upper() for word in words.split(",")]
    word_search = generate_word_search(words_list, min_size)
    return {"puzzle": word_search.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)