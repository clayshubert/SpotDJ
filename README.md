# SpotDJ
SpotDJ is a web app that uses AI to shuffle playlists from Spotify based on the audio statistics of each song to make the transitions between them sound seamless. It also includes an AI DJ mode that shuffles and mixes the highlights of each song to sound like a real DJ.

## Features
Simple Shuffle: Randomly shuffle the songs in the playlist.
AI Shuffle: Use AI to shuffle the playlist based on the audio statistics to create seamless transitions between songs.
AI DJ Mode: Use AI to select and mix the highlights of each song in real-time to sound like a professional DJ.
## Installation
To run SpotDJ, follow these steps:

1. Clone the repository to your local machine.
2. Create a Spotify developer account and create a new app to get your client ID and client secret.
3. Create a .env file in the root directory of the project and add your client ID and client secret to it in the following format:
~~~
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here 
~~~
4. Install the required Python packages using pip:
```pip install -r requirements.txt```
5. Run the app:
```python spotdj.py```

## Contributing
Contributions are welcome! If you have any suggestions for new features or improvements, please submit a pull request.

## License
SpotDJ is licensed under the MIT License. See LICENSE for more information.
