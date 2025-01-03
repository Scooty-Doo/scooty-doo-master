# scooty-doo-master
### ***Master repository for the Scooty-Doo application.***

#### *Managing Local Repository and Submodules Locally and Remotely:*

- **Clone repository with submodule references but without pulling submodule contents to local repository:**  

    git clone --recurse-submodules https://github.com/Scooty-Doo/scooty-doo-master

- **Initialize submodules in local repository, i.e. pull submodule contents to /submodules:**  

    git submodule update --init --recursive

- **Deinitialize submodules in local repository, i.e. keep submodule references but no longer keep submodule contents in local repository:**  

    git submodule deinit -f submodules/backend  
    git submodule deinit -f submodules/frontend  
    git submodule deinit -f submodules/bike

    **or...** 

    git submodule deinit -f --all  

- **Reinitialize (reset) submodules in local repository:**  

    git submodule deinit -f --all  
    git submodule update --init --recursive

- **Update submodule references to their latest commit:**  


    1. **Without pulling submodule contents to local repository or updating existing local submodule contents in /submodules:**  

        git submodule update --remote --no-fetch

    2. **By pulling submodules contents to local repository:**  

        2.1. ***Pull latest commit:***  
        git submodule update --remote --merge  

        **or...**

        git submodule foreach --recursive git pull origin main  

        **or if you want to update a specific submodule...**  

        git -C submodules/backend pull origin main  
        git -C submodules/bike pull origin main  
        git -C submodules/frontend pull origin main  

        2.2. ***Update remote master repository submodule references:***  
        git add submodules/*  
        git commit -m "Updated submodule references to latest commits"  
        git push origin main  



#### *Running the master application:*

- **Run the main application.**  
python -m src.main  
 
    In src.main.py under the "if __name__ == "__ main __"" block you can change Main(use_submodules) to True if you prefer using the /submodules folder instead of the /repositories folder.  
    
    You can also change main.run(skip_setup) to True if you want to skip setting up backend and bike (hivemind server), e.g. because you have already done so. This saves time when restarting the Main application.
