#-*- coding: utf8 -*-
import argparse
import requests
import os
import sys
#my develop version stravaweblib placed in ..//stravaweblib
try:
    from stravaweblib import StravaWebClient
except ImportError:
    sys.path.insert(0, "..//stravaweblib")
    from stravaweblib import StravaWebClient


try:
    from secret import STRAVA_LOGIN,STRAVA_PASSWORD
except ImportError:
    pass


class options():
    def __init__(self,usr, pwd, dest, actid):
        self.usr = usr
        self.pwd = pwd
        self.dest = dest
        self.actid = actid

def create_parser ():
    parser = argparse.ArgumentParser()
    # positional argument - strong required
    parser.add_argument("actid", type=int, help="strava action id")
    # named args - optional
    parser.add_argument ('-l', '--login',help="your strava login")
    parser.add_argument ('-p', '--password',help="your strava password")
    parser.add_argument ('-d', '--destination',help="destination dir to save photo")
 
    return parser

def parse_cli():
    parser = create_parser()
    args = parser.parse_args()
    user_login = args.login
    user_password = args.password
    user_actid = str(args.actid)
    user_destination = args.destination
    if not user_login :
        try: 
            user_login = STRAVA_LOGIN 
        except NameError: 
            user_login = input('login? :')

    if not user_password :
        try:
            user_password = STRAVA_PASSWORD
        except NameError: 
            user_password = input('password? :')

    return options(user_login, user_password, user_destination, user_actid)

def save_pic(url, name, dest_dir):
    p = requests.get(url)
    out_filename = os.path.join(dest_dir, name)+".jpg"
    out = open(out_filename, "wb")
    out.write(p.content)
    out.close()
        
if __name__ == '__main__':
    opt = parse_cli()
    strava_client = StravaWebClient()
    signed  = strava_client.login(opt.usr, opt.pwd)
    if signed:
        my_name=strava_client.get_my_name()
        print('login as: {}'.format(my_name))
        # destination dir
        if  opt.dest!=None:
            # check
            pass
        else:
            opt.dest = os.path.join(os.getcwd(), 'photo_'+opt.actid)
        if not (os.path.exists(opt.dest) and os.path.isdir(opt.dest)):
            # try to create
            os.makedirs(opt.dest)                
        print('destination dir: {}'.format(opt.dest))
        # get urls and download photo
        ph_urls = strava_client.get_activity_photo(opt.actid)
        for ph in ph_urls:
            ph_url = ph['large']
            ph_id = ph['photo_id']
            print('downloaded {}'.format(ph_id))
            save_pic(ph_url,ph_id, opt.dest)
    
    else:
        print('login fail :(')
        

    print('done!')     

    

