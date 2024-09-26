import sqlite3
from data_dict import random_users
from flask import Flask, jsonify, request
import requests


def createTable():
    #Connect to a (new) database
    with sqlite3.connect('members.db') as conn:
        #Create a cursor
        cur = conn.cursor()
        cur.execute(''' CREATE TABLE IF NOT EXISTS members
            (id INTEGER PRIMARY KEY , 
            first_name TEXT, 
            last_name TEXT,
            birth_date TEXT,
            email TEXT,
            phonenumber TEXT,
            address TEXT,
            nationality TEXT,
            active BOOLEAN,
            github_username TEXT
            )''')
        
        conn.executemany('''INSERT INTO members (
             first_name,
             last_name,
             birth_date,
             email,
             phonenumber,
             address,
             nationality,
             active,
             github_username
             ) VALUES (:first_name, :last_name, :birth_date, :email, :phonenumber, :address, :nationality, :active, :github_username)''', random_users)
    
        conn.commit()


def read():

    members = []
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append(i)

    return members


def updateUser(github_username, id):
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()

        cur.execute("UPDATE members SET github_username = ? WHERE id = ?", (github_username, id))
        conn.commit()

#GET all MEMBERS
def all_members():
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()

        cur.execute('SELECT id, first_name, last_name, github_username FROM members')
        members = cur.fetchall()
    return members


#FETCH REPO 
def fetch_github_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {
        "Authorization": "APIKEY"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200: 
        repos_data = response.json()

        return[{"name": repo["name"], "url": repo["html_url"]} for repo in repos_data]
    elif response.status_code == 404:
        return {"error": "Github username not found"}
    
    else: 
        return {"error": f'Failed to fetch repositories (status code: {response.status_code})'}

createTable()
        

       