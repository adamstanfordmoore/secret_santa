#!/usr/bin/env python3

"""
Secret Santa: send messages
@author Adam Stanford-Moore
@version 2017-12-14 
The script reads in the secret santa pairings and a list of email contacts and then
sends out an email to every person with the person they are paired with  
"""
import smtplib
import datetime
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MESSAGE = 'message.txt'
MY_ADDRESS = 'algebradam@gmail.com'
PASSWORD = 'animals77'
YEAR = datetime.datetime.now().year

def get_pairing(filename):
    #returns dictionary of {person: has_this_person}
    pairing = dict();
    names = [] 
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.rstrip('\n'))   
    
    first_name = names[0]            
    for i in range(len(names)):
        if (names[i] == '-'): 
            continue
        elif (i == len(names) - 1):
            pairing[names[i]] = first_name   
        elif (names[i+1] == '-'):
            pairing[names[i]] = first_name
            first_name = names[i+2] 
        else:
            pairing[names[i]] = names[i+1]
            
    return pairing

def get_contacts(filename):
    """
    Return a dictionary of 'name':'email_address'
    """
    contacts = dict()

    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            contacts[a_contact.split()[0]] = a_contact.split()[1]
    return contacts

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    year = str(YEAR)
    contacts = get_contacts('family_contacts.txt') # read contacts
    pairing = get_pairing('secret_pairings_' + year + '.txt') # read contacts
    message_template = read_template(MESSAGE)
    
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for person in pairing:
        msg = MIMEMultipart()       # create a message
        
        
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=person.title(), PAIRED_WITH=pairing[person].title(), THIS_YEAR=year)

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=contacts[person]
        msg['Subject']="SECRET SANTA " + year + "!"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg) #                    <---- ********** REALLY IMPORTANT *******
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()


