#-*- coding: utf8 -*-
import argparse
import requests
import os
import sys
from time import sleep

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
    def __init__(self,usr, pwd, ex_id):
        self.usr = usr
        self.pwd = pwd
        self.ex_id = ex_id


def create_parser ():
    parser = argparse.ArgumentParser()
    # named args - optional
    parser.add_argument ('-l', '--login',help="your strava login")
    parser.add_argument ('-p', '--password',help="your strava password")
    parser.add_argument ('-e', '--exclude', help='exclude athlete id', type=str)
  
 
    return parser

def parse_cli():
    parser = create_parser()
    args = parser.parse_args()
    user_login = args.login
    user_password = args.password
    if args.exclude:
        ex_id = [item for item in args.exclude.split(',')]
    else:
        ex_id=[]
        

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

    return options(user_login, user_password, ex_id)


if __name__ == '__main__':

    given_kudo=[]
    
    opt = parse_cli()

    excludes = opt.ex_id

    print('excludes : {}'.format(excludes))
    
    strava_client = StravaWebClient()
    signed  = strava_client.login(opt.usr, opt.pwd)
    if signed:
        my_id=strava_client.get_my_id()
        my_name=strava_client.get_my_name()
        print('login as: {} (id = {})'.format(my_name, my_id))
        followers = strava_client.get_followers(my_id)
        print('------followers----------')
        for f_id in followers:
            f_name = strava_client.get_name_athlethe(f_id)
            if (f_id in excludes) == 1:
                print('{} = {} - exluded!'.format(f_id, f_name))
                continue
            print('{} = {}'.format(f_id, f_name))
            print(excludes[0])
            act_list = strava_client.get_last_activities(f_id)
            for act in act_list:
                print('   -'+str(act))
                if strava_client.is_kudosable_activity(act):
                    #strava_client.give_kudo(act)
                    given_kudo.append((f_name, act))
                sleep(3) # 3 seconds
        print('-------------------------')

        print('KUDOS:')
        for gk in given_kudo:
            print(gk)
    else:
        print('login fail :(')
  
    print('done!')
    input('press enter')

    

