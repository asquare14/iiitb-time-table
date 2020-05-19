from flask import Flask
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from search import searchData
from datetime import timedelta, date 
import os
import itertools
import requests
import json
import re
import sys
import collections

DEPT_KEY = 'dept'
WEBSITE_KEY = 'website'
TIMETABLE_KEY = 'timetable'

timeMapStart = {}
timeMapEnd = {}
timeMapStart[0] = "09:30:00"
timeMapEnd[0] = "11:00:00"
timeMapStart[1] = "11:15:00"
timeMapEnd[1] = "12:45:00"
timeMapStart[2] = "14:00:00"
timeMapEnd[2] = "15:30:00"
timeMapStart[3] = "15:45:00"
timeMapEnd[3] = "17:15:00"