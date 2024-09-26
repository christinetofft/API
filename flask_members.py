from flask import Flask, jsonify, request
#from members import read, update, createTable
from members import read, updateUser, fetch_github_repos, all_members
app = Flask(__name__)


#GET 
@app.route('/members', methods = ["GET"])
def read_all():
    return jsonify(read())

#PUT 
@app.route('/members', methods=["PUT"])
def update():
    data = request.get_json()

    github_username = data.get('github_username')
    id = data.get('id')

    updateUser(github_username,id)

    return "Successful", 204

#GET REPO 
@app.route('/members/repos', methods=['GET'])
def getRepos():
    members = all_members()
    members_with_repos = []
    
    for member in members: 
        member_id, first_name, last_name, github_username = member

        if github_username:
            repos = fetch_github_repos(github_username)

        else:
            repos = []
        
        members_with_repos.append({
            "id": member_id,
            "name": f"{first_name}, {last_name}",
            "github_username": github_username,
            "repositories": repos
        })

    return jsonify(members_with_repos)


app.run(debug=True)
