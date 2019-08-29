#Udaciy Full Stack Web Development Linux Server Conf. Project

I created Linux Ubuntu Server in Amazon Lightsail 

SSH Key :
    <abbr title="Hyper Text Markup Language">DeinSSHKey.pem</abbr> 

You must add the key './ssh' folder

Username : ubuntu Ip : 18.195.67.211 (my server ip adress)

You connect "Connect using SSH" button.

You can connect also with this command on commandline :

'chmod 400 ~/.ssh/DeinSSHKey.pem'

'ssh -i ~/.ssh/DeinSSHKey.pem grader@18.195.67.211 -p 2200'

password : => 123456

- You cannot log in as root remotely : Completed

- The grader user can run commands using sudo to inspect files that are readable only by root : Completed

- Only allow connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) : Completed

- Key-based SSH authentication is enforced : Completed

- All system packages have been updated to most recent versions : Completed

- SSH is hosted on non-default port : Completed

- The web server responds on port 80 : Completed
 ( You can see you web site = `<link>` <http://18.195.67.211/> )

- Database server has been configured to serve data (PostgreSQL is recommended) : Completed

- Web server has been configured to serve the Item Catalog application as a WSGI app : Completed

* You can find Aws Lightsail settings und flask install requirements on resources

Resources

`<link>` <https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart>

`<link>` <https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps> 

`<link>` <https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04>

`<link>` <https://askubuntu.com/questions/673597/ssh-connect-to-host-127-0-0-1-port-2222-connection-refused/676057>

`<link>` <https://stackoverflow.com/questions/15722886/cant-ssh-as-root-into-ec2-server-please-login-as-the-user-ubuntu-rather-tha>

`<link>` <https://www.digitalocean.com/community/questions/error-permission-denied-publickey-when-i-try-to-ssh>

`<link>` <https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04-quickstart>

`<link>` <https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps>

Mete  | Demirtas
------------- | -------------
Udacity | Full Stack Web Development
Python  | Linux Server Configuration



