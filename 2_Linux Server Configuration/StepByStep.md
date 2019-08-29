#Udaciy Full Stack Web Development Linux Server Conf. Project

I created Linux Ubuntu Server in Amazon Lightsail 

SSH Key :
    <abbr title="Hyper Text Markup Language">DeinSSHKey.pem</abbr> 

You must add the key './ssh' folder

Username : ubuntu Public Ip : 3.121.208.166

I added static Ip : 18.195.67.211

You connect "Connect using SSH" button.

You can connect also with this command on commandline :

'chmod 400 ~/.ssh/DeinSSHKey.pem'

'ssh -i ~/.ssh/DeinSSHKey.pem ubuntu@18.195.67.211'

Firstly I need to admin password : 'sudo passwd' => 123456

Then I Added grader user : 'sudo adduser grader' => 123456

Grader must be in sudo group : 'sudo usermod -aG sudo grader'

'su - grader' => You can switch to user 

'sudo ls -la /root' => You can test sudo user

( `<link>` <https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart>)

Not finish yet, grader must be root user.

'su -' command make you root user.

On Root User :

'sudo visudo'

add to "etc/sudoers.tpm" => 'grader    ALL=(ALL:ALL) ALL'

( Artikel : How To Grant a User Sudo Privileges => 
`<link>` <https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps> )

In AWS Lightsail Networking windows I added '2200' and '123' Ports.

I must setup Firewall with UFW

'sudo ufw default allow incoming'
'sudo ufw default allow outgoing'

'sudo ufw allow ssh'
'sudo ufw allow http'
'sudo ufw allow ntp'
'sudo ufw allow 2200/tcp'

'sudo ufw enable'

( `<link>` <https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04>)

Now, I must change connection port. 22 => 2200

'sudo apt-get install ssh'

'sudo nano /etc/ssh/sshd_config'

You must chance '#Port 22' line to 'Port 2200'

Saved and 'sudo service ssh force-reload' command run.

Now you can't connect on port 22, you must use port 2200

'ssh -i ~/.ssh/DeinSSHKey.pem ubuntu@18.195.67.211 -p 2200'

( `<link>` <https://askubuntu.com/questions/673597/ssh-connect-to-host-127-0-0-1-port-2222-connection-refused/676057>)

If I want to login 'grader' user, I need to ssh key on grader user :

Add '.ssh' folder "/home/grader/.ssh" => 'sudo mkdir .ssh'

Copy AuthKey => 'sudo cp /home/ubuntu/.ssh/authorized_keys /home/grader/.ssh/'

( `<link>` <https://stackoverflow.com/questions/15722886/cant-ssh-as-root-into-ec2-server-please-login-as-the-user-ubuntu-rather-tha> )

* if you can't connect too.. then you can shown this article : 
 `<link>` <https://www.digitalocean.com/community/questions/error-permission-denied-publickey-when-i-try-to-ssh>

You can connect grader user :

''ssh -i ~/.ssh/DeinSSHKey.pem ubuntu@18.195.67.211 -p 2200''

It's time to install Apache Web Server and setting up virtual host :

'sudo apt update'

'sudo apt install apache2'

Now you can access apachi web server with this link = 18.195.67.211

Then virtual host : (my domain : cronyapp)

'sudo mkdir /var/www/cronyapp'

'sudo chown -R $USER:$USER /var/www/cronyapp'

'sudo chmod -R 755 /var/www/cronyapp'

'nano /var/www/cronyapp/index.html' => You can write html tags..

'sudo nano /etc/apache2/sites-available/cronyapp.conf'

you must fill :

"
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName your_domain
    ServerAlias your_domain
    DocumentRoot /var/www/your_domain
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
"

'sudo a2ensite cronyapp.conf'

'sudo a2dissite 000-default.conf'

'sudo systemctl restart apache2'

And restart apache server => 'systemctl reload apache2'

You can see you web site = 18.195.67.211

( `<link>` <https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04-quickstart> )

How can you database server install :

- Run these commands

```
    sudo apt-get -qqy install make zip unzip postgresql

    sudo apt-get -qqy install python3 python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install flask packaging oauth2client redis passlib flask-httpauth
    sudo pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests

    sudo apt-get -qqy install python python-pip
    sudo pip2 install --upgrade pip
    sudo pip2 install flask packaging oauth2client redis passlib flask-httpauth
    sudo pip2 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests

    sudo su postgres -c 'createuser -dRS grader'
    sudo su grader -c 'createdb'
    sudo su grader -c 'createdb forum'
```

We installed PostgreSQL and created 'forum' database.

And the last we must deploy a Flask application :

You must apply schrit by schrit this link = 
 `<link>` <https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps>

And then restart = 'systemctl reload apache2' => Your flask app is ready = 

`<link>` <http://18.195.67.211/>


Mete  | Demirtas
------------- | -------------
Udacity | Full Stack Web Development
Python  | Linux Server Configuration



