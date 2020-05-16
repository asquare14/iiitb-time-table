from flask import Flask
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from search import searchData
import os
import itertools
import requests
import json
import re
import sys
import collections