mkdir -p /usr/lib/community_datasets/
cp -r ./community_datasets/* /usr/lib/community_datasets/
cp -r ./cli.sh /usr/lib/community_datasets/
echo 'source /usr/lib/community_datasets/cli.sh' >> ~/.bashrc
