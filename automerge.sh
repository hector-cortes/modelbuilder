if [ "$TRAVIS_BRANCH" != "develop" ]; then
    exit 0;
fi

git config -- global user.name $GIT_NAME
git config -- global user.email $GIT_EMAIL

git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* || exit
git fetch --all || exit

git checkout master || exit
git merge --no-ff "$TRAVIS_COMMIT" || exit

git remote set-url origin "https://github.com/hector-crtes/modelbuilder.git"
git push origin master