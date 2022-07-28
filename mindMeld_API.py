#!/bin/bash/python
#-*- coding: utf-8 -*-

import json
import requests
import time



class mindMeld_API(object):

    server_data = {}
    server_data['mindmeld'] = {'header':  {'Accept': 'application/json; charset=UTF-8', 'Content-Type': 'application/json', },
                        'url':"http://54.88.72.6:7150/parse", }


    def __init__(self, env):

        self.url = self.server_data[env]['url']
        self.header = self.server_data[env]['header']



    def talk_to_assitant(self, conv):

        conversations = json.dumps(conv)
        response = requests.post(self.url, data=conversations, headers=self.header)
        print(response.text)
        if response and response.json():
            return response.json()
        return False



if __name__== "__main__":

    mindmeld_talking = mindMeld_API('mindmeld')
    with open('/home/jingaroo/Documents/test_conv.txt') as fp:
        convo_line = fp.readline()
        while convo_line:
            convo_line = fp.readline()
            #print(convo_line)
            conversation_text = {}
            conversation_text['text'] = convo_line
            mindmeld_talking.talk_to_assitant(conversation_text)
            time.sleep(30)
