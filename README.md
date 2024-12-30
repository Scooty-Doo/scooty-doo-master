# scooty-doo-master
Master repo for the Scooty-Doo app

To clone this repo along with all subrepos run:
git clone --recurse-submodules https://github.com/Scooty-Doo/scooty-doo-master

To get updated versions of the submodules you have to:
1. cd *name-of-subrepo*
2. git pull origin main

Then to update the master repo you have to commit the changes
1. cd .. (stand in master repo root)
2. git add *name-of-subrepo*
3. git commit -m "Update submodule reference for *name-of-subrepo*
4. git push origin main
