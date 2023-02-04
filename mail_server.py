from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import pathlib
import uuid
import json


app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute() # path to directory of this file

# Function to load and save the mail to/from the json file

def load_mail() -> List[Dict[str, str]]:
    """
    Loads the mail from the json file

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    try:
        return json.loads(thisdir.joinpath('mail_db.json').read_text())
    except FileNotFoundError:
        return []

def save_mail(mail: List[Dict[str, str]]) -> None:
    """
    
    Saves/Writes data from the mail to the given json file 
    with 4 spaces per level used to indent the content.
    
    Args:
    	mail (List[Dict[str, str]]): the given mail to save
    
    Returns:
    	Nothing
    """
    thisdir.joinpath('mail_db.json').write_text(json.dumps(mail, indent=4))
    

def add_mail(mail_entry: Dict[str, str]) -> str:
    """
    
    First load the current mail entries, then we append the new entries to the
    current dictionary. This can be done because mail is a list of dictionaires.
    Now add a key to mail_entry called "id" and an unique id value. We do this
    to identify/find this specific entry if we need to modify it. Finally we save
    the modified mail.
    
    Args:
    	mail_entry (Dict[str, str]): a new mail entry to add to mail
    
    Returns:
    	String: the unique id of the new added entry 
    
    """
    
    
    mail = load_mail()
    mail.append(mail_entry)
    mail_entry['id'] = str(uuid.uuid4()) # generate a unique id for the mail entry
    save_mail(mail)
    return mail_entry['id']

def delete_mail(mail_id: str) -> bool:
    """
    
    Deletes a specific mail, given its unique id. We go through all entries until
    we find the entry with the given id. Use pop(i) to delete it from the list. 
    Finally we save the modified mail. If the unique id was not found, the function will tell 
    the user that it failed because it could not delete anything.
    
    Args:
    	mail_id (str): A unique id to identify a mail entry that the user wants to delete
    
    Returns:
    	Bool: True if the id exists and was deleted, else False since nothing was found thus
    	not deleted.
    
    """
    mail = load_mail()
    for i, entry in enumerate(mail):
        if entry['id'] == mail_id:
            mail.pop(i)
            save_mail(mail)
            return True

    return False

def get_mail(mail_id: str) -> Optional[Dict[str, str]]:
    """
    
    Finds and returns a specific mail entry using the unique id it has when the entry was added.
    
    Args:
    	mail_id (str): A unique id to identify a mail entry that the user wants to find and return
    
    Returns:
    	Dict[str, str]: If the given id exists in mail, we return a dictionary containing
    	the information of that entry
    	
    	Nothing: If the given id does not exist in mail, nothing is returned.
 
    """
    mail = load_mail()
    for entry in mail:
        if entry['id'] == mail_id:
            return entry

    return None

def get_inbox(recipient: str) -> List[Dict[str, str]]:
    """
    Fetches all the mail that was sent to the given recipient. Utilizes the 'recipient' key
    in every mail entry to identify if the mail belongs in this recipients inbox. If so
    it appends it do a list of dictionaries called inbox.
    
    Args:
    	recipient (str): A given recipient to find and return all mails belong to him/her
    
    Returns:
    	List[Dict[str, str]]: A list of dictionaires that contains every mail entry that
    	was sent to the given recipient.
    
    """
    mail = load_mail()
    inbox = []
    for entry in mail:
        if entry['recipient'] == recipient:
            inbox.append(entry)

    return inbox

def get_sent(sender: str) -> List[Dict[str, str]]:
    """
    
    Fetches all the mail that have was sent by the given sender. Utilizes the 'sender' key
    in every mail entry to identify if the mail was sent by the given sender. If so it appends
    it do a list of dictionaires called sent.
    
    Args:
    	sender (str): A given sender to find and return all mails sent by him/her
    
    Returns:
    	List[Dict[str, str]]: A list of dictionaries that constains every mail entry that
    	was sent by the given sender.
    
    """
    mail = load_mail()
    sent = []
    for entry in mail:
        if entry['sender'] == sender:
            sent.append(entry)

    return sent

# API routes - these are the endpoints that the client can use to interact with the server
@app.route('/mail', methods=['POST'])
def add_mail_route():
    """
    Summary: Adds a new mail entry to the json file

    Returns:
        str: The id of the new mail entry
    """
    mail_entry = request.get_json()
    mail_id = add_mail(mail_entry)
    res = jsonify({'id': mail_id})
    res.status_code = 201 # Status code for "created"
    return res

@app.route('/mail/<mail_id>', methods=['DELETE'])
def delete_mail_route(mail_id: str):
    """
    Summary: Deletes a mail entry from the json file

    Args:
        mail_id (str): The id of the mail entry to delete

    Returns:
        bool: True if the mail was deleted, False otherwise
    """
    return jsonify(delete_mail(mail_id))
    

@app.route('/mail/<mail_id>', methods=['GET'])
def get_mail_route(mail_id: str):
    """
    Summary: Gets a mail entry from the json file

    Args:
        mail_id (str): The id of the mail entry to get

    Returns:
        dict: A dictionary representing the mail entry if it exists, None otherwise
    """
    res = jsonify(get_mail(mail_id))
    res.status_code = 200 # Status code for "ok"
    return res

@app.route('/mail/inbox/<recipient>', methods=['GET'])
def get_inbox_route(recipient: str):
    """
    Summary: Gets all mail entries for a recipient from the json file

    Args:
        recipient (str): The recipient of the mail

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    res = jsonify(get_inbox(recipient))
    res.status_code = 200
    return res

@app.route('/mail/sent/<sender>', methods=['GET'])
def get_sent_route(sender: str):
    """
    Summary: Gets all mail entries that a sender sent from the json file

    Args:
        sender (str): The sender of the mail

    Returns:
        list: A list of dictionaries representing the mail entries
    """
    res = jsonify(get_sent(sender))
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run(port=5000, debug=True)