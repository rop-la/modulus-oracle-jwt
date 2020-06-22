#!/bin/bash

openssl genrsa -out secrets/private.key 512
openssl rsa -in secrets/private.key -pubout -out secrets/public.key

chmod 775 secrets
chmod 664 secrets/*

docker run -it --rm \
    -v $(pwd)/html:/var/www/html \
    -v $(pwd)/secrets:/secrets \
    eboraas/apache-php
