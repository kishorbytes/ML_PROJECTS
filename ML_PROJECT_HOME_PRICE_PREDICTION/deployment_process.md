



1.Create EC2 instance using amazon console, also in security group add a rule to allow HTTP incoming traffic

2.Now connect to your instance using a command like this,

    ssh -i "C:\Users\Viral\.ssh\Banglore.pem" ubuntu@ec2-3-133-88-210.us-east-2.compute.amazonaws.com

3.nginx setup

    i.Install nginx on EC2 instance using these commands,
        sudo apt-get update
        sudo apt-get install nginx
    ii.Above will install nginx as well as run it. Check status of nginx using
        sudo service nginx status

    iii.Here are the commands to start/stop/restart nginx
        sudo service nginx start
        sudo service nginx stop
        sudo service nginx restart

    iv.Now when you load cloud url in browser you will see a message saying "welcome to nginx" This means your nginx is setup and running.


4.Now you need to copy all your code to EC2 instance. You can do this either using git or copy files using winscp. We will use winscp. You can download winscp from here: https://winscp.net/eng/download.php

5.Once you connect to EC2 instance from winscp (instruction in a youtube video), you can now copy all code files into /home/ubuntu/ folder. The full path of your root folder is now: /home/ubuntu/BangloreHomePrices

6.After copying code on EC2 server now we can point nginx to load our property website by default. For below steps,
    i.Create this file /etc/nginx/sites-available/bhp.conf. The file content looks like this,
        server {
            listen 80;
                server_name bhp;
                root /home/ubuntu/BangloreHomePrices/client;
                index app.html;
                location /api/ {
                    rewrite ^/api(.*) $1 break;
                    proxy_pass http://127.0.0.1:5000;
                }
        }

    ii.Create symlink for this file in /etc/nginx/sites-enabled by running this command,
        sudo ln -v -s /etc/nginx/sites-available/bhp.conf
    
    iii.Remove symlink for default file in /etc/nginx/sites-enabled directory,
        sudo unlink default
    iv.Restart nginx,
        sudo service nginx restart

7.Now install python packages and start flask server
    sudo apt-get install python3-pip
    sudo pip3 install -r /home/ubuntu/BangloreHomePrices/server/requirements.txt
    python3 /home/ubuntu/BangloreHomePrices/client/server.py

Running last command above will prompt that server is running on port 5000. 8. Now just load your cloud url in browser (for me it was http://ec2-3-133-88-210.us-east-2.compute.amazonaws.com/) and this will be fully functional website running in production cloud environment


Note: 
For more reference follow the video: https://www.youtube.com/watch?v=q8NOmLD5pTU&lc=Ugy7aUsKa2et8WYD8nd4AaABAg


C:\Users\Kishor\ML_Project\deployment_process.md