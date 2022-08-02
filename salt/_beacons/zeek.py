import logging


def status():

 cmd = "runuser -l zeek -c '/opt/zeek/bin/zeekctl status'"
 retval = __salt__['docker.run']('so-zeek', cmd)
 logging.info(f'zeekctl_module: zeekctl.status retval: {retval}')

 return retval


def beacon(config):

 retval = []

 is_enabled = __salt__['healthcheck.is_enabled']()
 logging.info(f'zeek_beacon: healthcheck_is_enabled: {is_enabled}')

 if is_enabled:
  zeekstatus = status().lower().split(' ')
  logging.info(f'zeek_beacon: zeekctl.status: {str(zeekstatus)}')
  zeek_restart = ('stopped' in zeekstatus or 'crashed' in zeekstatus
                  or 'error' in zeekstatus or 'error:' in zeekstatus)
  __salt__['telegraf.send'](f'healthcheck zeek_restart={zeek_restart}')
  retval.append({'zeek_restart': zeek_restart})
  logging.info(f'zeek_beacon: retval: {retval}')

 return retval

