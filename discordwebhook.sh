#!/bin/sh

#Change url to your discord webhook
#url = "https://discord.com/api/webhooks/<>"

curl -H "Content-Type: application/json" -X POST -d '{"content":"'"${domain} $1"'"}' $url

