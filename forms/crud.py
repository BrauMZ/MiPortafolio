from flask import Flask, render_template,request,redirect,url_for, Blueprint # For flask implementation
from bson import ObjectId    # For ObjectId to work
from pymongo import MongoClient
import os

crud = Blueprint('crud', __name__,
                        template_folder='templates')

cf_port = os.getenv("PORT")						

title = "CRUD Flask y MongoDB"
heading = "CRUD Python, Flask y MongoDB"

#mongodb://user_name:password@ip_host:port/Database_Name
#db = client.Database_Name
#table_var_name = db.table_name

client = MongoClient("mongodb://localhost:27017/taxis") #host uri
db = client.taxis                             #Select the database
todos = db.usuarios                           #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('crud')

@crud.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('crud.html',a1=a1,todos=todos_l,t=title,h=heading)

@crud.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('crud.html',a2=a2,todos=todos_l,t=title,h=heading)


@crud.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('crud.html',a3=a3,todos=todos_l,t=title,h=heading)

@crud.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	return redirect("crud.html")	
''' 	redir=redirect_url()	

	return redirect(redir) '''


@crud.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	nombre=request.values.get("nombre")
	email=request.values.get("email")
	celular=request.values.get("celular")
	id_tipo=request.values.get("id_tipo")
	todos.insert({ "nombre":nombre, "email":email, "celular":celular, "id_tipo":id_tipo, "done":"no"})
	return redirect("/list")

@crud.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("crud.html")

@crud.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@crud.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	nombre=request.values.get("nombre")
	email=request.values.get("email")
	celular=request.values.get("celular")
	id_tipo=request.values.get("id_tipo")
	_id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "nombre":nombre, "email":email, "celular":celular, "id_tipo":id_tipo, "_id":_id }})
	return redirect("crud.html")

@crud.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

#if __name__ == "__main__":

#    app.run()
if __name__ == '__crud__':
   if cf_port is None:
       crud.run(host='0.0.0.0', port=5000, debug=True)
   else:
       crud.run(host='0.0.0.0', port=int(cf_port), debug=True)    
