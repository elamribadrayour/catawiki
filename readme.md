# Catawiki Data Processing Project 📊

Welcome to the Catawiki Data Processing Project! This repository is designed to handle various aspects of processing Catawiki data, from scraping to embedding and exploring. Below you'll find a guide to each subdirectory and its purpose. 

## Table of Contents 📚
1. [Project Overview](#project-overview-)
2. [Subdirectories](#subdirectories-)
   - [catawiki-app](#catawiki-app-)
   - [catawiki-cache](#catawiki-cache-)
   - [catawiki-embed](#catawiki-embed-)
   - [catawiki-scrape](#catawiki-scrape-)
3. [Installation](#installation-)
4. [Usage](#usage-)
5. [Contributing](#contributing-)
6. [License](#license-)

## Project Overview 🌟

This project consists of several components aimed at processing and exploring data from Catawiki. Each component has a specific role, from scraping data to creating embeddings and visualizing insights. The project leverages modern technologies like Streamlit, DuckDB, and Transformers to provide a seamless experience.

## Subdirectories 📁

### 1. catawiki-app 🎨

- **Description:** This is a Streamlit application designed to explore Catawiki data and offer solutions such as recommendations and insights.
- **Technologies Used:** Streamlit, Python
- **Key Features:**
  - Interactive data exploration
  - Visualization of insights and trends
  - Recommendation engine

### 2. catawiki-cache 💾

- **Description:** This component deals with caching data using DuckDB to enhance performance.
- **Technologies Used:** DuckDB, Python
- **Key Features:**
  - Efficient data storage and retrieval

### 3. catawiki-embed 🖼️

- **Description:** This project focuses on embedding text and image data using Transformers to facilitate better data analysis and machine learning applications.
- **Technologies Used:** Sentence-Transformers, Python
- **Key Features:**
  - Text and image embeddings
  - Utilizes state-of-the-art transformer models

### 4. catawiki-scrape 🕸️

- **Description:** The scraping component responsible for collecting data from Catawiki.
- **Technologies Used:** Python, BeautifulSoup
- **Key Features:**
  - Automated data collection
  - Supports various data formats

## Installation 🛠️

To get started, clone this repository and install the necessary dependencies for each subdirectory:

```bash
git clone https://github.com/elamribadrayour/catawiki.git
cd catawiki-data-processing
```

To run each tast, navigate to its folder, build the container & run it:

```bash
cd catawiki-app
docker compose build
docker compose up
```

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
