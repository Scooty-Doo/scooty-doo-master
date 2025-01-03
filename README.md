# scooty-doo-master
Master repo for the Scooty-Doo app

# Method for cloning repo with submodule references but without checking out submodules contents.
git clone --recurse-submodules https://github.com/Scooty-Doo/scooty-doo-master

# Method for initializing submodules in local repo (pull contents to submodules folder):
git submodule update --init --recursive

# Method to deinitialize submodules in local repository (i.e. keep submodule references but no longer have the submodules contents in local repository):

git submodule deinit -f submodules/backend
git submodule deinit -f submodules/frontend
git submodule deinit -f submodules/bike

or 

git submodule deinit -f --all

# Method for reinitializing (resetting) submodules in local repo:
git submodule deinit -f --all
git submodule update --init --recursive

# Method for updating submodules references to the submodules last commit:
## Without pulling submodules contents to local repo:
git submodule update --remote --no-fetch

## By pulling submodules contents to local repo.
### 1. First pull latest commit.
git submodule update --remote --merge

or

git submodule foreach --recursive git pull origin main

or if you want to update a specific submodule

git -C submodules/backend pull origin main
git -C submodules/bike pull origin main
git -C submodules/frontend pull origin main

### 2. Then update remote master repo submodule references.
git add submodules/*
git commit -m "Updated submodule references to latest commits"
git push origin main
