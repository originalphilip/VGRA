# Server for Video Game Review Aggregator
The server for this project handles API requests from the client to fetch and manage video game reviews. It is built with Node.js and Express.

### Getting started

### Prerequisites
- Node.js (Download and install from [Node.js official website](https://nodejs.org/))
- npm (Comes installed with Node.js)

### Setup
After unzipping the repository to your local machine, navigate to the server directory:
'cd server'

### Installation
Install the necessary pacakges required for the server:
Make sure there is no current node_modules folder, if so delete this then do:
'npm install'

### Running the Server
To start the server:
'npm start'

This will launch the server on http://localhost:5000. 

If you already have something running on port http://localhost:5000, you can change this where http://localhost:5000 or port 5000 is defined in the code to another port number not being used.

Make sure that the server is running to handle requests from the client

### Running the Scripts

This application uses seperate Python Scripts to scrape game information and reviews from various sources. These scripts are essential for populating the database with up to date game reviews and related data.

### Review Scripts

The review scripts are located under the 'server/review_scrapers' directory. These scripts are responsible for collecting reviews from designated video game review websites. To update the reviews on the website, run each script as follows:

cd server/review_scrapers
python filename.py
Examples:
python IGNScraper.py # example for IGN reviews
python GameSpotScraper.py # example for GameSpot reviews

It is important to note that these review scripts should be run first to ensure that the database is populated with the latest reviews which are then used by the game script for fetching detailed game information.

### Game Script
After updating the reviews(shown above), run the game script located in the 'server/game_scraper' directory. This script collect detailed game information corresponding to the reviews collecte by the review scripts.

run the script as follows:
cd server/game_scraper
python IGDB.py

### Notes on Script Maintenance
Due to the nature of websites, changes to their structure such as updates to HTML or API changes may occur. Thefore, corresponding changes to the scripts will need to be made. Make sure that the scripts are maintained and updated regularly to keep the scraping process effective and data accurate. 
