## event type
##    var eventType = j.eventType;
##    var event = j.event
##
##
##    if (eventType == 'kudo') {
##        return $( "#kudo_template" ).tmpl( event )[0].innerHTML
##    }
##
##    if (eventType == 'activity') {
##        return $( "#solo_activity_template" ).tmpl( {"activity": event} )[0].innerHTML
##    }
##
##    if (eventType == 'comment') {
##        return $( "#comment_template" ).tmpl( event )[0].innerHTML
##    }
##
##    if (eventType == 'photo') {
##        return $( "#photo_template" ).tmpl( event )[0].innerHTML
##    }
##
##    if (eventType == 'clock') {
##        return $( "#clock_template" ).tmpl( event )[0].innerHTML
##    }
##
##    return "hi"




import json
import requests
import lxml.html

import websocket # pip install websocket-client
import time
from datetime import datetime

BASE_STRAVA_SITE_URL = 'https://www.strava.com'
login    = ''
password = ''


class athlete(object):
    def __init__(self, json_descript):
        annotation = json_descript['annotation']
        self.id        = json_descript['id']
        self.firstName = annotation['firstName']
        self.lastName  = annotation['lastName']
        self.sex       = annotation['sex']
    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)
        #return 'athlete({}, {}, {}, {})'.format(self.id, self.firstName, self.lastName, self.sex)
    def __repr__(self):
        return 'athlete({}, {}, {}, {})'.format(self.id, self.firstName, self.lastName, self.sex)


class activity(object):
    def __init__(self, json_descript):
        annotation = json_descript['annotation']
        self.id        = json_descript['id']
        self.athlete   = athlete(json_descript['athlete'])
        
        self.title     = annotation['title']
        self.activityType      = annotation['activityType']
        self.distance  = annotation['distance']
    def __str__(self):
        return '{}, {}, by {}'.format(self.activityType, self.title, str(self.athlete))
        #return 'act({}, {}, {}, {}), by {}'.format(self.id, self.activityType, self.title, self.distance,
        #                                           str(self.athlete))

class comment(object):
    def __init__(self, json_descript):
        annotation = json_descript['annotation']
        self.id       = json_descript['commentId']
        self.athlete  = athlete(json_descript['athlete'])
        self.activity = activity(json_descript['activity'])
        self.message  = annotation['message']
    def __str__(self):
        return '{}, say: "{}", for {}'.format(self.athlete, self.message, self.activity)

class kudo(object):
    def __init__(self, json_descript):
        self.athlete = athlete(json_descript['athlete'])
        self.activity = activity(json_descript['activity'])
    def __str__(self):
        return '{} kudoed {}'.format(self.athlete,  self.activity)

def extract_athletes_from_msg(obj, key):
    ath_list = []
    for k, v in obj.items():
        if k == key:
            print('find athlete')
            ath_list.append(athlete(v))
        elif isinstance(v, dict):
            ath_list.append(extract_athletes_from_msg(v, key))
        else:
            pass
    return ath_list

def filter():
    pass

def display_msg(msg):
    data = json.loads(msg) #загружаем из файла данные в словарь data
    print('---------  RAW MSG ---------------')
    print(msg)
    print('---------  ------- ---------------')
    print('---------  RAW DATA---------------')
    print(data)
    print('---------  ------- ---------------')    
    print('---------  EXTRACT ---------------')
    print(extract_athletes_from_msg(data, 'athlete'))
    print('---------  ------- ---------------') 
    
    #data = json.loads(msg) #загружаем из файла данные в словарь data
    typ = data['eventType']
    
    if typ == 'clock' :
        timestamp =data['event']['timestamp']
        date = datetime.fromtimestamp(timestamp)
        print('(T) {} {}'.format(timestamp, date))
    elif typ == 'kudo' :
        kudos = kudo(data['event'])
        timestamp = datetime.now().timestamp()
        print('(K) {}  at (T) {}'.format(kudos, timestamp))
    elif typ == 'comment' :
        comm = comment(data['event'])
        print('(C) {}'.format(comm))
    else :
        print(msg)

            
def strava_login(login,password):
    session = requests.session()
    r = session.get(BASE_STRAVA_SITE_URL+'/login/')
    cookies = r.cookies
    page = lxml.html.fromstring(r.content)
    form = page.forms[0]
    form.fields['email'] = login
    form.fields['password'] = password
    # add cookie
    session.cookies = cookies
    r = session.post( BASE_STRAVA_SITE_URL + form.action, data=form.form_values())
    cookies = session.cookies # <--- EEEEE this get _strava4_session
    plain_cookies = ";".join(["%s=%s" % (k, v) for k, v in cookies.items()])
    print(plain_cookies)

    name=''
    r = session.get( BASE_STRAVA_SITE_URL + '/athlete/calendar')
    parser = lxml.html.fromstring(r.text)
    lst_athlethe_name = parser.xpath("//title")
    if len(lst_athlethe_name)>0:
        name = lst_athlethe_name[0].text_content()
    first_name = name.split('|')
    print( first_name[1].strip() ) #first_name[1].strip()

    
    return plain_cookies

def on_message(ws, message):
##    print('--- raw msg ---')
##    print(message)
    display_msg(message)
##    data = json.loads(message) #загружаем из файла данные в словарь data
##
##    print(str(data['eventType'])+' : '+str(datetime.now()))
##    ath = athlete(data['event']['athlete'])
##    print(ath)
##    act = activity(data['event']['activity'])
##    print(act)


    
##  KUDO TYPE
##    {"event":
##         {"athlete":
##                   {"id":18507386, "annotation":{"firstName":"Eurípedes","lastName":"Leite MTB","sex":"M"}},
##          "activity":
##                   {"id":1091733837,
##                    "athlete":{"id":9232885,"annotation":{"firstName":"Alexander","lastName":"Kristoff","sex":"M"}},
##                    "annotation":{"title":"Lunch Ride","activityType":"Ride","distance":186262.0}}},
##     "eventType":"kudo"}

##    COMMENT TYPE
##      {"event":
##           {"commentId":261400429,
##            "athlete":
##                    {"id":10858560,"annotation":{"firstName":"Luis Mario","lastName":"Mesa","sex":"M"}},
##            "activity":
##                    {"id":1091516638,
##                     "athlete":{"id":4044192,"annotation":{"firstName":"Javi","lastName":"Moreno","sex":"M"}},
##                     "annotation":{"title":"17 etapa Tour de France","activityType":"Ride","distance":182076.0}},
##            "annotation":{"message":"Excelente etapa Dani"}},
##       "eventType":"comment"}

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    main()

def on_open(ws):
    ws.send("Hello from py" )
    pass


def main():
    print('Login to Strava...')
    auth_plain_cookies = strava_login(login,password)
    print('Connect to minifeed...')
    my_header=["Cookie:"+auth_plain_cookies]
    
    websocket.enableTrace(True)
    #ws = websocket.WebSocketApp("ws://localhost:9001/",
    #ws = websocket.WebSocketApp("wss://minifeed.strava.com/websocket/?athleteId=19600970/",
    ws = websocket.WebSocketApp("wss://minifeed.strava.com/websocket/",
                              header = my_header,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    

if __name__ == "__main__":
    main()



