import MySQLdb
import os
import image_process

def connect_MySQL():

    user_db = MySQLdb.connect(host="localhost", user="root", passwd="1234")

    cursor = user_db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS  EC601_MiniProject3_db")
    cursor.execute("use EC601_MiniProject3_db")
    cursor.execute("CREATE TABLE  IF NOT EXISTS user_record (username VARCHAR(20), nImgs INT, labels TEXT)")

    return cursor


def add_account(cursor):
    #account =  "@taylorswift13"
    account = input("Enter a new tweeter account: ")
    cursor.execute("SELECT * FROM user_record WHERE username= %s" % (account))
    match = cursor.fetchall()
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

    sql = "INSERT INTO user_record (username, nImgs, labels) VALUES (%s, %s, %s)"
    values = (account, nPics, all_labels)
    cursor.execute(sql, values)


def query_account(cursor):
    #account = "@taylorswift13"
    account = input("Enter an added account")
    cursor.execute("SELECT * FROM user_record WHERE username= %s" % (account))
    match = cursor.fetchall()
    if not match:
        print("No match found!")
    else:
        for row in match:
            print("account =", row[0], "\nnImgs=", row[1], "\nlabels=", row[2])


def delete_account(cursor):
    #account = "@taylorswift13"
    account = input("input an account to delete")
    cursor.execute("SELECT * FROM user_record WHERE username= %s" % (account))
    match = cursor.fetchall()
    if not match:
        print("This account has been added")
    else:
        cursor.execute("DELETE FROM user_record WHERE username= %s" % (account))

def search_label(cursor):
    label = input("Enter a label to search: ")
    cursor.execute(("SELECT * FROM user_data"))
    match = cursor.fetchall()
    print('Following usernames have this label:')
    for row in match:
        labels_temp = row[2].split(',')
        if label in labels_temp:
            print(row[0])


def get_all_and_most_common(cursor):
    cursor.execute("SELECT * FROM user_data")
    match = cursor.fetchall()
    labels = {}
    if match:
        print('There are' + len(match) + 'records:')
        for row in match:
            print('account=' + row[0], 'nImgs=' + row[1])
            labels_temp = row[2].split(',')
            for single_label in labels_temp:
                if single_label in labels.keys():
                    labels[single_label] += 1
                else:
                    labels[single_label] = 0
        most_common = max(labels.items(), key=lambda x: x[1])[0]
        print('the most common label is ' + most_common)
    else:
        print("The data is empty")