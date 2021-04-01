mkdir -p /usr/lib/community_datasets/
cp -r ./community_datasets/* /usr/lib/community_datasets/
sudo chmod +x /usr/lib/community_datasets/engine.py
echo 'alias community_datasets=/usr/lib/community_datasets/engine.py' >> ~/.bashrc
