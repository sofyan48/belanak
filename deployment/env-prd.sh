#!/bin/bash
vault kv get -format=json production/prd-belanak | jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' >> .env