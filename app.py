from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient

import os
from dotenv import load_dotenv

# Will load all the environemnt variables 
#load_dotenv()

# This must be the name of this function
def create_app():

    app = Flask(__name__)
    #client = MongoClient("mongodb+srv://RVA:myfirstdbMicroblog@microblog-cluster.w0yhr.mongodb.net/")
    client = MongoClient(os.getenv("MONGODB_URI"))

    # Saving the database named "microblog" in the app
    app.db = client.microblog


    # Everytime we restart the app , entries list will become empty.
    # entries = []

    """
    Tells Flask that this endpoint might receive POST as well as GET requests.
    """
    @app.route("/", methods=["GET", "POST"])
    def home():

        """
        we've got a request that's coming in to this function.

        It might be one of two requests.

        (i) It might be the browser loading the page i.e., render the template home.html.

        (ii) request that's coming over to this function as a result of the user submitting the form.
            We want to grab the field contents and do something with that data.
        
        """

        # The request variable is a value that has something inside it, whenever we're in a 
        # function that is currently responding to a request.
        if request.method == "POST" :

            """
            Remember that when the form submits the data, it is added to a payload and sent
            with a request, and we can access that data with request.form.get content.

            request.form : is a dictionary
            """

            entry_content = request.form.get("content")
            formatted_date = ""
            if entry_content : 
                formatted_date = datetime.datetime.today().strftime("%d-%m-%Y")

                #print(entry_content, formatted_date)
                # entries.append((entry_content, formatted_date))
                #print(entries[0][0])
                #print(entries[0][1])

                # Saving in the Mongodb cloud
                app.db.entries.insert_one(
                                    {"content" : entry_content ,
                                    "date" : formatted_date}
                                    )
                
        entries_with_date = [(
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%b %d")
                    ) for entry in app.db.entries.find({})]
                   
  
            #print(entries)

        return render_template( "home.html", entries= entries_with_date )
    
    return app













