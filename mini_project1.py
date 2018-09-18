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

consumer_key = "dXrq8z9Ph6MZaoO4aIphPY7EA"
consumer_secret = "QB06nE5KvYqc9gdRPDSJvsqtzCHFeaPFXL4EHp2Bzpm1C00J0U"
access_key = "1039356566519074817-iFnyvMWjjJLEf1OEkAq9wCrehgtFBu"
access_secret = "jyYdMngKjFrM8yeJs8HzkIjsPHntwTlQPTB2EpR67fJFk"


def download_pics(path, username, nPics):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    twt_api = tweepy.API(auth)

    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".jpg"):
                    os.remove(os.path.join(root, name))
    except FileNotFoundError:
        pass

    if not os.path.exists(path):
        os.mkdir(path)

    nTweets = 200
    counter = 0
    while counter < nPics-1:
        tweets = twt_api.user_timeline(screen_name=username, count=nTweets)
        for i in range(nTweets):
            try:
                media_contents = tweets[i].entities["media"]
                for content in media_contents:
                    if content["media_url"][-3:] in ["jpg", "png", "bmp"]:
                        pic_url = content["media_url"]
                        pic = req.get(pic_url).content

                        open(path + '/' + str("%03d" % counter) + '.jpg', 'wb').write(pic)
                        print(counter)
                        counter = counter+1
            except KeyError:
                pass
            if counter > nPics-1:
                break


def convert_pics_2_video(nPics, path):

    for i in range(nPics):
        pic = Image.open(path + '/' + str("%03d" % i) + ".jpg").resize([500, 500])
        pic.save(path + '/' + str("%03d" % i) + '.jpg')
        print(i)

    path_video = os.getcwd() + "/twitter_video.mp4"
    if os.path.exists(path_video):
        os.remove(path_video)

    subprocess.run(['ffmpeg', '-f', 'image2', '-i', 'twitter_pics/%*.jpg', '-r', '5', 'twitter_video.mp4'])

def google_vision_api(nPics):
    client = vision.ImageAnnotatorClient()

    path_result = os.getcwd() + '/picture_lables.txt'
    if os.path.exists(path_result):
        os.remove(path_result)

    f_results = open(path_result, 'w')

    for i in range(nPics):
        file_name = os.path.join(os.path.dirname(__file__), 'twitter_pics/' + str("%03d" % i) + '.jpg')

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)


        response = client.label_detection(image=image)
        labels = response.label_annotations

        print(i)

        f_results.write('Picture '+ str(i) +'\n')
        for label in labels:
            f_results.write(label.description + '\n')
        f_results.write('\n')

def main():

    nPics = 50
    username = "@taylorswift13"
    path = os.getcwd() + '/twitter_pics'

    #download_pics(path, username, nPics)

    #convert_pics_2_video(nPics, path)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/sean/EC601/MiniProject1/EC601HW1-1f6d3fdb0675.json"
    google_vision_api(nPics)

if __name__ == '__main__':
    main()
