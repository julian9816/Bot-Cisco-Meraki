import os
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json
from webexteamssdk import WebexTeamsAPI
import webexteamssdk

# Retrieve required details from environment variables
bot_email = "JACS@webex.bot"
teams_token = "YzY2Mzk5MGEtNjBjOC00MGQzLTg0ZGEtNDYxOTc0YWY5MzgwZTA4MTcxMTUtNTg3_PF84_aa304639-0f78-4b61-b684-a6bfff52067a"
bot_url = "http://aa5f193a.ngrok.io"
bot_app_name = "JACS"
api = WebexTeamsAPI(access_token='YTkzYmY3NjMtNDdiZC00YjE2LTk4YTYtYTZlYjZjZTY0ODlkN2RiNTVhYjktODE0_PF84_aa304639-0f78-4b61-b684-a6bfff52067a')
# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)

def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hola {}, yo soy un chat bot. ".format(sender.firstName)
    response.markdown += "Mira lo que yo puedo hacer, escrbiendo el siguiente comando **/help**."
    return response
# A simple command that returns a basic string that will be sent as a reply
def do_something(incoming_msg):
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return "Hice lo que dijiste - {}".format(incoming_msg.text)

def createuser(incoming_msg):
    response = Response()
    datosus=incoming_msg.text.split('/createuser')
    print(datosus)
    if datosus[1]=='':
        response.text="Por favor utilice el comando de la siguiente manera: \n/createuser Email: \nNombre a mostrar: \nNombres: \nApellidos: \nOrganizacion:\nLicencias(Separadas por un guion):"
    else:
        datosus=incoming_msg.text.split('/createuser')[1]
        datos=datosus.split('\n')
        info=[]
        for n in datos:
            info.append(n.split(':')[1])
        emails=[]
        emails.append(info[0])
        people=api.people.create(emails, displayName=info[1], firstName=info[2], 
                          lastName=info[3])
        print(type(people))
        if type(people) is webexteamssdk.models.immutable.Person:
            response.markdown="El usuario ha sido creado con exito"
        else:
            response.markdown="Ha ocurrido un error creando el usuario, por favor verifique los valores"
    return response

def ret_message(incoming_msg):
 
    # Create a object to create a reply.
    response = Response()

    # Set the text of the reply.
    response.text = "Here's a fun little meme."

    # Craft a URL for a file to attach to message
    u = "https://sayingimages.com/wp-content/uploads/"
    u = u + "aaaaaalll-righty-then-alrighty-meme.jpg"
    response.files = u
    return response

# Add new commands to the box.
bot.add_command("/dosomething", "Ayuda hacer algo", do_something)
bot.add_command("/createuser", "Ayuda a crear un usuario", createuser)
bot.add_command("/demo", "Crea un mensaje demo.", ret_message)
bot.set_greeting(greeting)

if __name__ == "__main__":
    # Run Bot
    bot.run(host="127.0.0.1", port=5000)
