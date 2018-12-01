#!/usr/bin/env python
# encoding: utf-8

import tweepy
import requests as req
import os
from PIL import Image
import subprocess
import io
from google.cloud import vision
from google.cloud.vision import types

# You may need to use your own authorization for twitter API
twitter_consumer_key = "your_consumer_key"
twitter_consumer_secret = "your_consumer_secret"
twitter_access_key = "your_access_key"
twitter_access_secret = "your_access_secret"

# 50 images are required
nPics = 50


def download_pics(path, username, nPics):

    # Get authorization of twitter pi
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_key, twitter_access_secret)
    twt_api = tweepy.API(auth)

    # Delete images from the last download
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".jpg"):
                    os.remove(os.path.join(root, name))
    except FileNotFoundError:
        pass

    # Create the directory for images
    if not os.path.exists(path):
        os.mkdir(path)

    nTweets = 200 # Download 200 tweets as a batch every time
    counter = 0

    # Keep downloading images until the required number of images is met
    while counter < nPics-1:
        tweets = twt_api.user_timeline(screen_name=username, count=nTweets)

        # Search and save the images from the 200 tweets
        for i in range(nTweets):
            try:
                media_contents = tweets[i].entities["media"]
                for content in media_contents:
                    if content["media_url"][-3:] in ["jpg", "png", "bmp"]:

                        # Download the image
                        pic_url = content["media_url"]
                        pic = req.get(pic_url).content

                        # Save the image
                        open(path + '/' + str("%03d" % counter) + '.jpg', 'wb').write(pic)
                        print("Saving picture: ", counter)
                        counter = counter+1

            except KeyError:
                pass
            if counter > nPics-1:
                break


def convert_pics_2_video(nPics, path):

    # Resize the images
    for i in range(nPics):
        pic = Image.open(path + '/' + str("%03d" % i) + ".jpg").resize([500, 500])
        pic.save(path + '/' + str("%03d" % i) + '.jpg')
        print("Resizing images: ", i)

    path_video = os.getcwd() + "/twitter_video.mp4"
    if os.path.exists(path_video):
        os.remove(path_video)

    # Implement FFMPEG
    subprocess.run(['ffmpeg', '-f', 'image2', '-i', 'twitter_pics/%*.jpg', '-r', '5', 'twitter_video.mp4'])


def google_vision_api(nPics):

    client = vision.ImageAnnotatorClient()

    # Delete the result from last time
    path_result = os.getcwd() + '/picture_lables.txt'
    if os.path.exists(path_result):
        os.remove(path_result)

    all_labels = ""
    f_results = open(path_result, 'w')

    # Generate labels for each image with google could vision api
    for i in range(nPics):

        file_name = os.path.join(os.path.dirname(__file__), 'twitter_pics/' + str("%03d" % i) + '.jpg')
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        # Implement google cloud vision api
        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print("Analyzing images: ", i)

        # Save the result to a file
        f_results.write('Picture '+ str(i) +'\n')
        label_temp = ""
        for label in labels:
            #f_results.write(label.description + '\n')
            label_temp += ',' + label.description
        label_temp = label_temp[1:]
        f_results.write(label_temp + '\n' + '\n')
        all_labels += label_temp + '\n'

    all_labels = all_labels[:-1]
    return all_labels


def main():


    twitter_username = "@taylorswift13"
    path = os.getcwd() + '/twitter_pics'

    #download_pics(path, twitter_username, nPics)
    #convert_pics_2_video(nPics, path)

    # Set the environment for google cloud vision api, you may need to change it to your own local google credential file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/your_credentials_file"
    google_vision_api(nPics)

if __name__ == '__main__':
    main()
