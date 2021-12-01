Steps to making secret Santa list:
1. change who is in INCLUDED_IN_DRAW - number is family id so you don’t get paired with someone from same family
2. make sure all contacts in family_contacts are accurate
3. change backdoor in generate_pairings to add/remove people
4. generate_pairings
5. edit message.txt -> this is the message to be sent out
6. test send_messages.py with the send line commented out
7. send_messages.py


Files in folder:
family_contacts.txt - name email associations

generate_pairings_standard.py - reads in INCLUDED_IN_DRAW.txt and the last two years of pairings and creates the random pairings. Standard version doesn’t have any added features to make pairings with lots of specifications through backdoor.

generate_pairings.py includes a time_out catch for the find_pairings recursive method.  Also includes a change that looks for people with few possible partners and chooses them earlier in the random drawing to make the pairing faster.     

INCLUDED_IN_DRAW - all people to be included

message.txt - message template to be sent out

secret_pairings_YEAR.txt - pairings for each year so you can’t get someone you got in the last two years.  Each person on the list is assigned the person below them - bottom person with top person. 

send_messages - reads in the secret_pairings_YEAR.txt, family_contacts.txt, and message.txt to send emails 

simple_email - practice sending short emails, unrelated  