#!/bin/bash
vault kv get -format=json staging/stg-belanak | jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' >> .env