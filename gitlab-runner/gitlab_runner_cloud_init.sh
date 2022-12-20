#!/bin/bash
# piclos-selenium
### Ubuntu 20.04

sudo apt update -y
sudo apt upgrade -y

sudo apt -y install apt-transport-https xdg-utils fonts-liberation libxkbcommon0 libxdamage1 libpango-1.0-0 libnss3 libgtk-3-0 libgbm1
sudo apt -y install unzip gcc g++ make yarn libasound2 
sudo apt -y install vim git yarn python-is-python3 python3-pip

curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g selenium-side-runner

curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

pip install poetry

sudo npm install -g jest
#sudo npm install -g chromedriver
#yarn global add chromedriver

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
google-chrome --version

wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver 
sudo chmod +x /usr/bin/chromedriver


sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
sudo chmod +x /usr/local/bin/gitlab-runner
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo rm /home/gitlab-runner/.bash_logout

sudo shutdown -r now