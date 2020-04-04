import json
import os
import random
import re

from variables import helpPage
from pathlib import Path

basePath = Path(os.getcwd()).parent
commandPath = basePath / "commands" 

commands = []

identifier = "{}"
timeRange = range(2,11)

def generate_description(args):
    body = ""
    if (len(args) == 0):
        for commandFile in os.listdir(commandPath):
            f = open(commandPath / commandFile)
            commandsJson = json.loads(f.read())
            f.close()
            line = commandFile.split(".")[0]
            try:
                body += """<b>{}</b>:<br>
{}<br>
<br>
""".format(line, "    " + commandsJson["description"])
            except:
                body += """<b>{}</b>:<br>
There is no description for this category yet.<br>
<br>
""".format(line, commandsJson["description"])
    
    else:
        print(args)
        for line in args:
            if len(line) == 0 or line.isspace():
                continue
           
            try:
                f = open(commandPath / (line.strip().lower() + ".json"))
                commandsJson = json.loads(f.read())
                f.close()
                body += """<b>  {}</b>:
    {}

""".format(line, commandsJson["description"])
            except:
                body += "Couldn't find a description for " + line + "\n\n"
            
    return body

def generate_help():
    body = helpPage.format(generate_description([]))
    return body

def insert_time(command):
    if identifier in command:
        return command.format(random.choice(timeRange))
    return command

def generate_commands(lines, amountCommands):
    pictures = False
    pickedCommands = []
    for line in lines:
        if line.isspace() or line == "":
            continue
        commandsJson = None
        parts = None
        if re.findall("body.writing", line.lower()):
            parts = line.split(" ")
            f = open(commandPath / "body-writing.json")
            commandsJson = json.loads(f.read())
            f.close()
            writingLine = commandsJson["commands"]
            texts = commandsJson["texts"]
            parts.pop(0)
            pickedCommands += list(map(lambda str: writingLine[0].format(random.choice(texts)) + str, parts))
        elif re.findall("pictures", line.lower()):
            pictures = True
        else:
            try: 
                f = open(commandPath / (line.strip().lower() + ".json"))
                commandsJson = json.loads(f.read())
                f.close()  
                pickedCommands += commandsJson["commands"]
            except:
                print("Couldn't open or find " + str(commandPath) + line.strip().lower())
                continue

    random.shuffle(pickedCommands)
    amount = min(int(amountCommands), len(pickedCommands))
    responseBody = list(map(lambda str: insert_time(str) + "<br>", pickedCommands[0:amount]))
    if pictures:
        f = open(commandPath / "pictures.json")
        commandsJson = json.loads(f.read())
        f.close()
        responseBody.append("".join(commandsJson["commands"]))
        
    return "".join(responseBody)
