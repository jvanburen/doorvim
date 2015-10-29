#!/usr/bin/vm shell -S /usr/bin/python

# The MIT License (MIT)
# Copyright (c) 2015 Jacob Van Buren

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import division

from user import *
from interface import Vgetty
from time import sleep
import logging
import sys ###

HELLO = None  # "sounds/prompt.m4a"  # Convert to modem format
UNAUTH = None  # "sounds/no.m4a"  # Convert to modem format
GOODBYE = None  # "sounds/goodbye.m4a"  # Convert to modem format
LOG_FILE = '/users/jacob/Desktop/visitors.log'  # '/home/pi/visitors.log'

class Doorvim(Vgetty):
  def unlock(self):
    self.dial("#9")

def main():
  users = load_users()
  doorvim = Doorvim()

  code = doorvim.read_dtmf_string(prompt=HELLO)
  if code is None:
    doorvim.play(GOODBYE)
    return 0
  user = authenticate_user(code, users)
  if user is None:
    LOG.info(" Unauthorized user entered code: '%s'" % code)
    doorvim.play(UNAUTH)
    sleep(0.5)
  else:
    LOG.info(" recognized user %s" % user.name)
    doorvim.play(user.greeting)
    doorvim.unlock()
  doorvim.play(GOODBYE)

  del doorvim
  Vgetty.finalize()
  return 0

if __name__ == '__main__':
  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  logging.info("Starting " + __name__)
  LOG = logging.getLogger(__name__)

  retc = main()
  # logging.shutdown()
  exit(retc)



