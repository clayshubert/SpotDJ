# SpotDJ
SpotDJ is a web app that uses AI to shuffle playlists from Spotify based on the audio statistics of each song to make the transitions between them sound seamless. It also includes an AI DJ mode that shuffles and mixes the highlights of each song to sound like a real DJ.

## Features
Simple shuffle a selected playlist:
Use Spotify Web API to authenticate and get access to a user's playlists.
Allow the user to select a playlist they want to shuffle.
Use the Spotify Web API to get the list of tracks in the playlist and shuffle them randomly.
Play the shuffled playlist using Spotify playback SDK.
Use AI to shuffle the playlist based on the audio statistics to make the transitions sound seamless:
Use a Python library like Librosa or TensorFlow to extract audio features like tempo, key, and energy from each song in the playlist.
Use a machine learning algorithm like k-nearest neighbors or a neural network to predict the best order for the songs based on their audio features to create seamless transitions.
Play the shuffled and AI-enhanced playlist using Spotify playback SDK.
AI DJ mode that shuffles the songs and mixes the highlights of each song to sound like a real DJ:
Use the same audio feature extraction and machine learning algorithms as in feature 2 to predict the best order for the songs in the playlist.
Use another machine learning algorithm like a Markov chain or a reinforcement learning agent to select and mix the highlights of each song in real-time to sound like a real DJ.
Play the AI DJ mode playlist using Spotify playback SDK and possibly display visualizations of the transitions and mixing on a web interface.
## Installation
To run SpotDJ, follow these steps:

Clone the repository to your local machine.
Create a Spotify developer account and create a new app to get your client ID and client secret.
Create a .env file in the root directory of the project and add your client ID and client secret to it in the following format:
makefile
Copy code
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
Install the required Python packages using pip:
Copy code
pip install -r requirements.txt
Run the app:
Copy code
python app.py
## Contributing
Contributions are welcome! If you have any suggestions for new features or improvements, please submit a pull request.

## License
SpotDJ is licensed under the MIT License. See LICENSE for more information.
