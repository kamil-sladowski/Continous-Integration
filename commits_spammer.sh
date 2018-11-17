#!/bin/bash


if [ $# -eq 0 ]; then
 echo "Provide token, username, repository and number of commits"
 exit 1
fi

token=$1
username=$2
controlled_repository=$3
commit_number=$4

echo "$token"
echo "$username"
echo "$controlled_repository"

#token="72faa47f2280b202f8b2b2b7169369b2857138a9"
#username="Project-temporary-user"
#controlled_repository="watching-repository"
current_dir=`pwd`

if ! [ -d ${controlled_repository} ]; then
mkdir ${controlled_repository}
git clone "https://github.com/$username/$controlled_repository.git" ${controlled_repository}
cd ${controlled_repository}
git remote set-url origin "https://$username:${token}@github.com/$username/$controlled_repository.git"
fi


cd "$current_dir/$controlled_repository"
for i in `seq $commit_number`; do
    echo `date '+%Y%m%d%H%M%S'` > README.md
    git add README.md
    git commit -m "new code change"
    git push origin master
    sleep 5
done