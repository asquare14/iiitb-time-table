from flask import Flask, Response
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
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
from ics import Calendar, Event


DEPT_KEY = 'dept'
WEBSITE_KEY = 'website'
TIMETABLE_KEY = 'timetable'
