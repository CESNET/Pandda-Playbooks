#!/bin/bash

PROG=/usr/bin/dpdk-hugepages.py
CONF=/etc/ipfixprobe/hugepages.cfg

if [ "$1" = "start" ]; then
   if $PROG -s | grep -q '^[0-9]'; then
      echo already allocated;
   else
      SIZE=$(cat "$CONF")
      if [[ "$SIZE" == ?(-)+([[:digit:]]) && "$SIZE" -ge 1 && "$SIZE" -lt 255 ]]; then
         $PROG -p 1G --setup "${SIZE}G"
      else
         echo "Bad SIZE ($SIZE) in $CONF: should be a number 1 <= SIZE <= 255." >&2
         exit 1
      fi
   fi
elif [ "$1" = "stop" ]; then
   $PROG -u
   $PROG -c
else
   echo "Unknown parameter, use $0 start|stop."
   exit 1
fi
