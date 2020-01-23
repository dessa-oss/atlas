#!/bin/sh

echo "This script will edit your latest commit with the new initials and git issue number provided."
echo "Source this script by running it with '. rename_latest_commit.sh' to have the proper environment variables set for your next commits.\n"
exec < /dev/tty

printf "Enter your initials: "
read GIT_AUTHORS
export GIT_AUTHORS=$GIT_AUTHORS

printf "Enter the git issue number: "
read GIT_ISSUE_NUM
export GIT_ISSUE_NUM=$GIT_ISSUE_NUM

OLD_MSG=`git log -1 --pretty=%B`

git commit --amend -m ${OLD_MSG#*| }
