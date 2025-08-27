# Find Your Movies

Project related to the examination of AI Lab: Computer Vision and NLP of the academic year 2024/2025. The project is organized by the following students:
- Biancalana Alessio
- Cimarelli Alessandro 
- Della Scala Stefano 

Find Your Movies – Movies Recognition and Analysis from Poster

A computer vision project that identifies a movie from its poster and displays its information and recommendations.

📌 Description
====================

The program is designed to analyze posters of movies. It aims to recognize the film, providing information regarding title, 
year, duration, rating, genre(s), director, studio, cast, plot summary and recommend similar movies based on textual similarity.


📁 Project Structure
====================

```plaintext
📁 project_root/
├── Data/
    ├── Posters/                # Movie poster images
    ├── Raw/                    # Raw CSV files (movies, genres, actors, studios...)
    └── metadata.csv            # Movie info: title, ID, genres...
├── GUI/
    ├── app.py                  # Tkinter main application entry point
    ├── main_window.py          # Main window layout and interface logic
    └── tooltip.py              # Tooltip widget for enhanced user interaction
├── Scripts/
    ├── build_dir.py            # Extract director information from crew.csv
    ├── generate_collage.py     # Create poster collage for background
    └── recommend.py            # Content-based recommendation logic
| 
├── requirements.txt            # Project dependencies
├── build_metadata.py           # Merge raw CSV files into metadata.csv
├── extract_features_cnn.py     # Extract visual features using ResNet50 (CNN)
└── README.md                   # Project documentation
```

⚙️ How It Works
====================

The project is structured into three main components, namely:

* **Feature Extractor**
  
    Visual feature extraction is performed using ResNet50, a deep convolutional neural network pretrained on ImageNet. The classification head is removed, and the output of the final pooling layer (2048-dimensional vector) is used as a compact representation of the visual content of the poster.

    The process is as follows:
  -	Posters are loaded and resized to 224×224 pixels.
  -	Normalization is applied using the mean and standard deviation of ImageNet.
  - Feature vectors are extracted individually for simplicity.
  - Extracted vectors are stored in 'features.npy', with corresponding IDs in 'ids.npy'.


  This embedding allows the system to represent visual style, composition, and color distribution in a dense numerical format, which is used for similarity comparison via cosine distance.

  **Accuracy of Visual Recognition**

  The ResNet-50 module demonstrated a strong ability to correctly identify movies from input posters. In qualitative tests across the dataset, the system consistently matched posters to their corresponding movies, even when images had slight variations in quality or resolution.

  While quantitative evaluation was not the primary focus, the visual recognition accuracy exceeded expectations, with ResNet50 embeddings correctly retrieving the intended movie in most cases. The main sources of error were posters with highly abstract artwork or minimal textual/visual cues, which reduced the distinctiveness of the extracted features.

  A recurring issue was observed with film franchises or sequels that share very similar poster designs. This behavior highlights the challenge of distinguishing between movies in the same series when their posters share nearly identical stylistic and compositional patterns.

* [Recommender](Scripts\README.md)
* [GUI](GUI\README.md)


Installation
====================

**Clone**
    
    https://github.com/AlessioBiancalana/AiLab-Project.git

**Install dependencies**

    # Core scientific stack
    numpy
    pandas
    scikit-learn

    # Deep learning and feature extraction
    torch
    torchvision

    # Image processing
    Pillow
    opencv-python

    # GUI
    tkinter


How to run
====================

Before running the application, make sure you have installed all dependencies listed in `requirements.txt`.

You can go to [build_metada](build_metadata.py) and change LIMIT and put a number from 0 to 500 for the maximum number of movies that are used

1. **Build the metadata file**  
    
    From the project root, run:
        
        python build_metadata.py

    This script merges the raw CSV files into a single metadata.csv.

2. **Extract visual features with ResNet50**

    Run:
        
        python extract_features_cnn.py

    This will generate the feature embeddings (features.npy and ids.npy) for all posters.

3. **Launch the GUI**

    Start the application with:

        python -m GUI.app

4. **Use the app**

    Once the GUI is open, upload a movie poster.
    You can use any poster image stored inside the folder:

        Data/Posters/
    or one of the images in the project root

Future improvements
====================
- Use of CLIP or other multimodal transformers for joint image-text embedding spaces.
- Hybridization with collaborative filtering for enhanced personalization.
- Deployment as a web application for broader accessibility.
