#!/usr/bin/env python

import os
from decouple import config

user = config('username')
password = config('password')

print(user)
print(password)