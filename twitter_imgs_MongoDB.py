import pymongo
import os
import image_process


def add_account():
    #account =  "@taylorswift13"
    account = input("Enter a new tweeter account: ")

    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    database = connect["EC601_MiniProject3_db"]
    myset = database["user_record"]

    match = myset.find({'username': account})
    if match:
        print("This account has been added")
        return

    nPics = image_process.nPics
    path = os.getcwd() + '/twitter_pics'

    print("Downloading images from tweeter")
    image_process.download_pics(path, account, nPics)

    print("Converting images to video")
    image_process.convert_pics_2_video(nPics, path)

    print("Analyzing the images")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/sean/Documents/EC601/MiniProject1/EC601HW1-1f6d3fdb0675.json"
    all_labels = image_process.google_vision_api(nPics)

    new_account = {"username": account, "nImgs": nPics, "labels": all_labels}
    myset.insert_one(new_account)


def query_account():
    #account = "@taylorswift13"
    account = input("Enter an added account")
    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    database = connect["EC601_MiniProject3_db"]
    myset = database["user_record"]
    match = myset.find({'username': account})
    if not match:
        print("No match found")
    else:
        for row in match:
            print("account =", row['username'], "\nnImgs=", row['nImgs'], "\nlabels=", row['labels'])


def delete_account():
    #account = "@taylorswift13"
    account = input("input the account to delete")
    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    database = connect["EC601_MiniProject3_db"]
    myset = database["user_record"]
    match = myset.find({'username': account})
    if not match:
        print("No match found")
    else:
        myset.remove({'username': account})


def search_label():
    label = input("Enter a label to search: ")
    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    database = connect["EC601_MiniProject3_db"]
    myset = database["user_record"]
    print('Following usernames have this label:')
    for row in myset.find():
        labels_temp = row['labels'].split(',')
        if label in labels_temp:
            print(row['username'])


def get_all_and_most_common():
    connect = pymongo.MongoClient("mongodb://localhost:27017/")
    database = connect["EC601_MiniProject3_db"]
    myset = database["user_record"]
    labels = {}
    print('There are' + myset.count() + 'records:')
    for row in myset.find():
        print('account='+row['username'], 'nImgs='+row['nPics'])
        labels_temp = row['labels'].split(',')
        for single_label in labels_temp:
            if single_label in labels.keys():
                labels[single_label] += 1
            else:
                labels[single_label] = 0
    most_common = max(labels.items(), key=lambda x: x[1])[0]
    print('the most common label is ' + most_common)