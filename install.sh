mkdir -p /usr/lib/community_datasets/
cp -r ./* /usr/lib/community_datasets/
echo 'source /usr/lib/community_datasets/cli.sh' >> ~/.bashrc
export PYTHONPATH=/usr/lib/community_datasets/
