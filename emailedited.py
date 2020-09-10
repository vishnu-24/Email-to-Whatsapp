import imaplib
import email
from email.header import decode_header
from twilio.rest import Client
import datetime 


def canContinue(date):
    recivedDate=' '
    if date[6]!=' ':
        recivedDate=date[5]+date[6]
        recivedMonth=date[8:11]
        recivedYear=date[12:16]
    else:
        recivedDate='0'+date[5]
        recivedMonth=date[7:10]
        recivedYear=date[11:15]

    recivedDate=int(recivedDate)
    recivedYear=int(recivedYear)
    temp = datetime.datetime.now()
    currentMonth = temp.strftime('%b')
    currentMonth=currentMonth.lower()
    recivedMonth=recivedMonth.lower()
    currentDate=int(datetime.datetime.now().day)
    currentYear=int(datetime.datetime.now().year)
    
    if currentMonth==recivedMonth and currentYear==recivedYear:
        if currentDate==recivedDate:
            return 1
        elif (currentDate-1)==recivedDate:
            return 1
        else:
            return 0
        
    else:
        return 0
     

def gmail(last_email_id,imap):
    attachment=0
    html=0
    var=0
    bodyText=" "
    
    res, msg = imap.fetch(str(last_email_id), "(RFC822)")

    for response in msg:
        if isinstance(response, tuple):
           
            msg = email.message_from_bytes(response[1])
            
            subject = decode_header(msg["Subject"])[0][0]
            date = decode_header(msg["date"])[0][0]
            if isinstance(subject, bytes):
                
                subject = subject.decode()
            if isinstance(date, bytes):
                
                date = date.decode()
            from_ = msg.get("From")
               
            var=canContinue(date) 
            
            if(var==1):
                pass
            elif(var==0):
                break
            
            if isinstance(subject, bytes):
                
                subject = subject.decode()
                
            
            from_ = msg.get("From")
            
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                
                    except:
                        pass
                    if (content_type == "text/plain") and ("attachment" not in content_disposition):
                        bodyText=bodyText + body
                    elif "attachment" in content_disposition:
                        attachment=1
                
                
                        
            else:
                content_type = msg.get_content_type()
                body = msg.get_payload(decode=True).decode()
                
                if content_type == "text/plain":
                  bodyText=bodyText+body
            if content_type == "text/html":
                    html=1
            return subject,from_,bodyText,attachment,html,var
    return subject,from_,bodyText,attachment,html,var


def result(output,reciver):
        if(output[5]==0):
             return 1
        else:
        
            account_sid = 'Your twilio sid'
            auth_token = 'your twilio Token'
            client = Client(account_sid, auth_token)
                                      
            if (output[3]==1 and output[4]==1):
                message = client.messages.create(
                                          body='From: '+output[1]+"\n"+'Subject: '+output[0]
                                          +"\n"+'Body: '+output[2][0:200]+'..continue reading in mail'+"\n"+'Attachment found..check ur email for more details'+"\n"
                                            +'html link found ... plz check ur email for more details'  ,
                                          from_='whatsapp:+14155238886',
                                          to='whatsapp:{}'.format(reciver)
                                      )
                 
            elif (output[4]==1):
                message = client.messages.create(
                                          body='From: '+output[1]+"\n"+'Subject: '+output[0]
                                          +"\n"+'Body: '+output[2][0:200]+'..continue reading in mail'+"\n"
                                            +'html link found ... plz check ur email for more details'  ,
                                          from_='whatsapp:+14155238886',
                                          to='whatsapp:{}'.format(reciver)
                                      )
            elif (output[3]==1):
                message = client.messages.create(
                                          body='From: '+output[1]+"\n"+'Subject: '+output[0]
                                          +"\n"+'Body: '+output[2][0:200]+'..continue reading in mail'+"\n"
                                            +'Attachment found..check ur email for more details'  ,
                                          from_='whatsapp:+14155238886',
                                          to='whatsapp:{}'.format(reciver)
                                      )
            else:
                message = client.messages.create(
                                          body='From: '+output[1]+"\n"+'Subject: '+output[0]
                                          +"\n"+'Body: '+output[2][0:200]+'..continue reading in mail'
                                                  ,
                                          from_='whatsapp:+14155238886',
                                          to='whatsapp:{}'.format(reciver)
                                      )



def login(username,password,reciver): 
    
        imap = imaplib.IMAP4_SSL("imap.gmail.com",993)
        try:
            imap.login(username, password)
        except Exception as e:
            print("Invalid creadenticals for:",username)
        else:
            imap.select("[Gmail]/Important") #if u want to select inbox use:imap.select("Inbox")
            status, messages = imap.search(None, '(UNSEEN)')
            if(status=="OK"):
                mail_ids =messages[0]
                id_list = mail_ids.split() 
                idl=[]
                first_email_id = int(id_list[0])
                latest_email_id = int(id_list[-1])
                for a in range(0,len(id_list),1):
                    item=int(id_list[a])
                    idl.insert(a,item)
                
                for x in range(latest_email_id,first_email_id-1,-1):
                    for i in range(len(idl)):
                        if idl[i] == x:
                            isthere=1
                            break
                        else:
                            isthere=0
                    if(isthere==1):
                            output=gmail(x,imap)
                            a=result(output,reciver)
                            if(a==1):
                                break
    
            imap.close()
            imap.logout()
                    
                    
            
            
            
if __name__=="__main__":
    
    users=["emailid1","password1","Phonenumber"]#you can add multiple user details in this list
    for x in range(0,len(users),3):
        login(users[x],users[x+1],users[x+2])

    
    
