#!/bin/bash
vault kv get -format=json development/dev-belanak | jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' >> .env