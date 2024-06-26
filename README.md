# Word Search Puzzle API

## Description

The Word Search Puzzle API generates customizable word search puzzles using FastAPI. It supports placing words horizontally, vertically, diagonally, and in reverse. Users can specify words and optionally set a minimum grid size. Puzzles are returned in JSON format for easy integration into applications.

## Features

- Generate word search puzzles with specified words
- Supports horizontal, vertical, diagonal, and backward word placements
- Configurable minimum grid size
- Efficient word placement using concurrency
- Random letter fill for remaining grid spaces

## Installation

To install and run the Word Search Puzzle API, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/CesarEnc/word-search-puzzle-api
   cd repository

2. **Install Dependencies:**:
Install the required packages using pip and the requirements.txt file:

   ```bash 
   pip install -r requirements.txt
## Usage

1. **Run the FastAPI Application**:

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app:app --reload