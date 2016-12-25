#!/bin/env python
# -*- coding: utf-8 -*-

import shlex
import base64

class Utils:
    @staticmethod
    def removeDQuotes(string):
        '''remove double quotes of string'''
        if string:
            string = string.replace('"', '')
        return string

    @staticmethod
    def escapedquotes(string):
        '''escape " to \" '''
        if string:
            string = string.replace('"', '\\"')
        return string
    
    @staticmethod
    def base64_encode(string):
        '''convert string to base64 formated'''
        return base64.encodestring(string.encode('utf-8'))
    
    @staticmethod
    def base64_decode(string):
        ''' decode base64 formated string'''
        return base64.decodestring(string).decode('utf-8')
