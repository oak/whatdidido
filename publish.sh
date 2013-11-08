rsync -avz ./* -e 'ssh -p 21 -i ../../adcarvalho_ec2.pem' ubuntu@worksynergist.com:/var/www/whatdidido/ --exclude '*.pyc' --exclude '.idea' --exclude '.hg*' --exclude '.git*'
