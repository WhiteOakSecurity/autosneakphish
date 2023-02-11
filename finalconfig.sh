#!/bin/bash
sudo certbot certonly --standalone -d go_substring1.domainstring1 --register-unsafely-without-email --agree-tos --non-interactive --expand
sudo cp /etc/letsencrypt/live/go_substring1.domainstring1/fullchain.pem /home/ubuntu/gophish/go_substring1.domainstring1.crt
sudo cp /etc/letsencrypt/live/go_substring1.domainstring1/privkey.pem /home/ubuntu/gophish/go_substring1.domainstring1.key
sudo sed -i 's/example.crt/go_substring1.domainstring1.crt/g'  /home/ubuntu/gophish/config.json
sudo sed -i 's/example.key/go_substring1.domainstring1.key/g'  /home/ubuntu/gophish/config.json
sudo sed -i 's/80/443/g'  /home/ubuntu/gophish/config.json
sudo sed -i 's/false/true/g'  /home/ubuntu/gophish/config.json
sudo bash -c 'cd /home/ubuntu/gophish && go build'
sudo bash -c 'cd /home/ubuntu/gophish && nohup /home/ubuntu/gophish/gophish &'
