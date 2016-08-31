# SaltWeb
A web interface for SaltSatck. In this Platform, we can 

# dependence
Webpy
Mako
MySQLdb
SaltStack
python-dmidecode
psutil

# How to install
1. yum update:
Make your yum repository is in the latest state. There are many methods which can achieve this goal. So you just choose the best method you like.
2. Install salt:
For installing the salt-stack, I think that the best document is the salt official documentation. You can access that from [this link](https://docs.saltstack.com/en/latest/)
I will put the installation process for CentOS 5 in this place.
    1. Run the following commands to install the SaltStack repository and key:
        wget https://repo.saltstack.com/yum/redhat/salt-repo-latest-1.el5.noarch.rpm
        sudo rpm -ivh salt-repo-latest-1.el5.noarch.rpm
        rm -f salt-repo-latest-1.el5.noarch.rpm
    2. Run sudo yum clean expire-cache:
        sudo yum clean expire-cache
    3. Install the salt-minion, salt-master, or other Salt components:
        sudo yum install salt-master
        sudo yum install salt-minion
        sudo yum install salt-api
        (If you are a cautious guy, you can find that salt has some other components. We just use these three, but I suggest you try the other one.)
3. Install mysql:
    It is good in your favorite way. :) Just make sure that you have a mysql in your ENV.
    After installed the mysql, you need change the file "config/database.py". You need change the mysql user, password and database name for yourself.
4. Install the python dependency packages:
    As we all know, there are many dependency management tools in python. You can just use your favorite one. In this place, I prefer pip.
    pip install web.py
    pip install Mako
    yum install MySQL-python
    yum install python-dmidecode
    pip install psutil
5. Run the salt web project
    python run.py [your prefer port]




