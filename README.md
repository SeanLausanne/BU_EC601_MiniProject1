# BU_EC601_MiniProject1

This is the first mini project of the course EC601 of Boston University.

The project contains 3 major parts:<br>
  Downloading images with Twitter API<br>
  Convert to the images to a video with FFMPEG<br>
  Analyze the images with Google Could Vision API<br> 

The file is written in Python 3.5. Before running, please make sure that you have installed these libraries: tweepy, PIL, google-cloud-vision.<br>

The function "download_pics" downloads a required number of images from a twitter account(Taylor Swift, in this case). Then the images are saved to a local directory "twitter_pics".<br>

The function "convert_pics_2_video" turns all the images to a mp4 video saved at the same directory.<br>

The function "google_vision_api" uses Google Cloud Vision APi to analyze all the images. The API gives several labels to each picture. The results are saved in picture_labels.txt
