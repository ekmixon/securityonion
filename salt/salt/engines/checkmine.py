# -*- coding: utf-8 -*-

import logging
from time import sleep
from os import remove

log = logging.getLogger(__name__)

def start(interval=30):
  log.info("checkmine engine started")
  minionid = __grains__['id']
  while True:
    try:
      ca_crt = __salt__['saltutil.runner']('mine.get', tgt=minionid, fun='x509.get_pem_entries')[minionid]['/etc/pki/ca.crt']
      log.info('Successfully queried Salt mine for the CA.')
    except:
      log.error('Could not pull CA from the Salt mine.')
      log.info(
          f'Removing /var/cache/salt/master/minions/{minionid}/mine.p to force Salt mine to be repopulated.'
      )
      try:
        remove(f'/var/cache/salt/master/minions/{minionid}/mine.p')
        log.info(f'Removed /var/cache/salt/master/minions/{minionid}/mine.p')
      except FileNotFoundError:
        log.error(f'/var/cache/salt/master/minions/{minionid}/mine.p does not exist')

      __salt__['mine.send'](name='x509.get_pem_entries', glob_path='/etc/pki/ca.crt')
      log.warning('Salt mine repopulated with /etc/pki/ca.crt')

    sleep(interval)