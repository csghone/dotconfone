#!/bin/bash
############################################################
#
############################################################

case "$1" in
    logout)
        i3-msg exit
        ;;
    suspend)
        lock && systemctl suspend
        ;;
    reboot)
        systemctl reboot
        ;;
    poweroff)
        systemctl poweroff
        ;;
    *)
        echo "Usage: $0 {lock|logout|suspend|reboot|poweroff}"
        exit 2
esac

exit 0
