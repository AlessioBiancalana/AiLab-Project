# AiLab-Project

Project related to the examination of AI Lab: Computer Vision and NLP of the academic year 2022/2023. The project is organized by the following students:
- Alessio Biancalana
- Alessandro Cimarelli
- Stefano Della Scala

Poster2Movie – Film Recognition and Analysis from Poster

A computer vision project that identifies a movie from its poster and displays its information and recommendations.

📌 Description
====================

Poster2Movie is an intelligent application that:
- Recognizes a movie from its poster image
- Automatically retrieves:
  - Title
  - Release date
  - Runtime
  - Rating (IMDb/TMDB)
  - Genre
  - Production studio
  - Main cast
  - Plot
- Recommends similar movies based on genre

The project combines Image Processing, Computer Vision, Deep Learning, and integration with external APIs.

🔧 Technologies
====================

- Python 3.x
- OpenCV / Pillow – image processing
- TensorFlow / Keras – feature extraction with CNN
- scikit-learn – similarity search
- TMDB API – movie metadata
- Streamlit – user interface

📁 Project Structure
====================

project_root/
│
├── data/
│   ├── posters/              # Movie poster images
│   └── metadata.csv          # Movie info: title, ID, genres...
│
├── features/
│   └── poster_features.npy   # Poster image feature vectors
│
├── scripts/
│   ├── fetch_posters.py      # Download posters via TMDB API
│   ├── extract_features.py   # Extract features using CNN
│   ├── match_poster.py       # Match uploaded poster to dataset
│   ├── fetch_metadata.py     # Retrieve movie metadata
│   └── recommend.py          # Recommend similar movies
│
├── app.py                    # Streamlit web app
├── requirements.txt
└── README.txt


⚙️ How It Works
====================

1. The user uploads a movie poster image.
2. The system compares the image to a local poster database using visual features.
3. Once the match is found, the TMDB API is queried to retrieve detailed movie data.
4. The movie information is displayed.
5. Recommendations for similar movies are shown.



