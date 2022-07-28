#!/bin/bash/python
# -*- coding: utf-8 -*-

#import json
#import requests
#import csv
#import time


"""
class RocketChat(object):


    server_data = {}
    server_data['live'] = {'header':  {'Accept': 'application/json', 'Content-Type': 'application/json'},
                           'url': "http://localhost:3000/api/v1/",
                           }
    server_data['dev'] = {'header':  {'Accept': 'application/json', 'Content-Type': 'application/json'},
                          'url': "http://localhost:3000/api/v1/",
                         }



    def __init__(self, env):

        self.url = self.server_data[env]['url']
        self.header = self.server_data[env]['header']



"""
    #def get_users_info(self, token, user_id):
         """
            Retrieves information about a user
          :param user_id:
          :return: Json DATA or False
         """

         #response = requests.get(self.url + "users.info?userId=" + user_id , headers=self.header)
         #print(response.text)
         #if response and response.json() and token:
            #return response.json()
         #return False




    #def create_users(self, token, user_id, user_info):
         """
           Create user
          :param user_info:
          :return: Id or False
         """
         #newUsers = json.dumps(user_info)
         #response = requests.post(self.url + "users.create", data=newUsers, headers=self.header)
         #print(response.text)
         #if response and response.json() and token:
            #return response.text
         #return False



    #def delete_users(self, token, user_id, userIDorName):
         """
           Delete user
          :param user_info:
          :return: Id/name or False
         """
         #existing = json.dumps(userIDorName)
         #response = requests.post(self.url + "users.delete", data=existing, headers=self.header)
         #print(response.text)
         #if response and response.json() and token:
            #return response.text
         #return False



#Login authorization
    #def loginAuth(self, login_info):
        """
        Login with your username and password.

         :param name:
         :return: Id or False
        """
        #assert login_info is not None

        # Data
        #data_json = json.dumps(login_info)
        #response = requests.post(self.url + "login", data=data_json, headers=self.header)
        #print(response.text)
        #print(response.status_code)

        #if response.ok:
            #responseMap = response.json()
            #authToken = responseMap['data']['authToken']
            #self.header['X-Auth-Token']=authToken
            #self.header['X-User-Id']= responseMap['data']['me']['_id']
            #return True
        #return False



    #def personalToken(self, token, user_id, token_name):
        """
        With the addition of the ability to generate personal access tokens,
        you can use the REST API without having to sign in.
        """
        #data_json = json.dumps(token_name)
        #response = requests.post(self.url + "users.generatePersonalAccessToken", data=data_json, headers=self.header)
        #print(response.text)
        #if response and response.json() and token:
            #return response.json()
        #return False



    #def createChannel(self, token, user_id, channel_name):
        """public channels"""
        #data_json = json.dumps(channel_name)
        #response = requests.post(self.url + "channels.create", data=data_json, headers=self.header)
        #print(response.text)
        #if response and response.json() and token:
            #return response.json()
        #return False



    #def createGroups(self, token, user_id, group_name):
        """private groups"""
        #data_json = json.dumps(group_name)
        #response = requests.post(self.url + "groups.create", data=data_json, headers=self.header)
        #print(response.text)
        #if response and response.json() and token:
            #return response.json()
        #return False



    #def groupInvite(self, token, user_id, invitation):
        """invites users to the private group"""
        #data_json = json.dumps(invitation)
        #response = requests.post(self.url + "groups.invite", data=data_json, headers=self.header)
        #print(response.text)
        #if response and response.json() and token:
            #return response.json()
        #return False




"""
Test
if __name__== "__main__":
    log_info       = {}
    log_info["user"]   = ""
    log_info["password"]   = ""
    rocket_service = RocketChat('live')
    DidLogIn = rocket_service.loginAuth(log_info)
    if DidLogIn == True:
        #rocket_service.get_users_info(DidLogIn,'')
        #channel_name = {}
        #channel_name['name'] = ""
        #rocket_service.createChannel(DidLogIn,'',channel_name)
        #group_name = {}
        #group_name['name'] = ""
        #rocket_service.createGroups(DidLogIn, '',group_name)
        #invitation = {}
        #invitation['roomId'] = ""
        #invitation['userId'] = ""
        #rocket_service.groupInvite(DidLogIn,'', invitation)
        #with open('users.txt','r') as file:
            #stripped = (line.strip() for line in file)
            #lines = (line.split(",") for line in stripped if line)
            #with open('users.csv','w') as outFile:
                #writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #writer.writerow(('name','email','password','username'))
                #writer.writerows(lines)
        with open('users.csv') as file:
            users_obj = csv.reader(file)
            next(file) #skip header row
            for row in users_obj:
                print("row:{0}".format(row))
                user_info = {}
                user_info["name"] = row[0]
                user_info["email"]   = row[1]
                user_info["password"]   = row[2]
                user_info["username"]   = row[3]
                rocket_service.create_users(DidLogIn, 'HhefrQTGzBLEsZY9o', user_info)
                time.sleep(50)
        #userID = {}
        #userID['userId']='m2EWZ8E7wSjZX3Pb4'
        #rocket_service.delete_users(DidLogIn,'HhefrQTGzBLEsZY9o',userID)
        #user_info["name"]   = ""
        #user_info["email"]   = ""
        #user_info["password"]   = ""
        #user_info["username"]   = ""
        #rocket_service.create_users(DidLogIn, 'Td6NZDxHFLJpJGRCr', outFile)
        #token_name = {}
        #token_name["tokenName"] = ""
        #print(rocket_service.personalToken(DidLogIn, 'HhefrQTGzBLEsZY9o', token_name))
"""
