# Git strategy

This document defines certain strategies to be followed with our git project. At the end of the document there is a file, `Useful commands for git.md`, that defines some of the most common commands you might use when something unexpected happens and you need to reset.


There are different strategies in git usually, 

1. Rebase/cherry-pick trying to keep a linear history
2. Commit merge

We have decided to go with a commit-merge strategy. We are going to abuse gitlab, to make it easier!


Before we go any further, make sure you use the right global git configuration.

	# configure email and username
	git config —global user.email “<your_gitlab_email>"
    git config —global user.name “<your_username>”
    # configure editor, nano or any editor you have installed you prefer
    git config --global core.editor "nano" 



## Summary

Basically, the procedure is simple:

1. Master is never touched
2. you make a branch called `explore-*`, `refactor-*`, `test-*`, etc, so the name explains what you did, `git checkout -b <branch-name>`
3. If you want to add large file into working area, please track it with LFS `git lfs track "path_to_large_file"` before adding it into stage area. (In detail, please read the part `Git large file storage` below)
3. You commit your changes to that branch `git add .; git commit`
4. You push to gitlab `git push -u origin HEAD`
5. You follow the link that gitlab gives you to request a merge request to the repository
6. If there are conflicts... you solve them in gitlab directly
7. You are done!

**NOTE: Remember to do `git checkout master; git pull --all` every morning to be up-to-date with all the changes. :)**


## Master shall not be touched


Master shouldn't be touched:

1. No committing to master any changes directly
2. No merging into master locally
3. Everything is done through merge requests. (If you do something to it, since the branch is protected in gitlab, you will have errors every time you time to fetch from gitlab)
4. **All merges to master should be done through a merge request**. 

## Merging strategy


### Commit merge strategy.


We are going to use merge commit with no fast forward, to keep a history that reflects the changes and the history of the project.

For that, if you are going to use the command `git merge` at any point, add to them a `--no-ff`, like so

	git merge --no-ff 
	# Prevents merge from doing fast forward
	
I hope we can do most merges through gitlab, but in small changes in branches, merging different branches, it might be useful to use `git merge`

### Procedure


1. Commit all your changes, _(this is a lot easier using a UI than the terminal... I use a UI when possible. (Rstudio/Visual Studio Code/Pycharm/Eclipse, ...))_
	- With a UI: Follow the instruction on screen, add the files you need to the `.gitignore` files and continue until the status of unstaged things is clean. 
 
	- Without a UI:
	
		+ Add files
	
			```
			git status # check the current status
			git add <files-to-commit>
			
			```
		+ If there are some files you don't want to commit never, consider adding a `.gitignore` in that folder, or in the folder above to ignore them.
		
		+ Run `git status` one last time and make sure there are no files that are unstaged. (If there are files you don't want to commit, you don't want to ignore them, etc, use `git stash` to stash them.
		
	
	- After the `git status` reports something clean, finally:
			
		```
		git commit
		```
	
	
2. Before pushing anything, make sure you are up to date

	```
	git checkout master
	git pull --all 
	# Pulls master and other branches, 
	# and makes our local branches catch up to them.
	```

1. Move to the branch we want to push

		git checkout <branch-to-merge> 
		
2. Then push that branch to a branch on the remote with the same name:

		git push -u origin HEAD 

	Yes, just copy this command, with the word `HEAD`. `HEAD` means _"Current branch I am checking right now"_ for git.
	
3. Check in gitlab the project, and go to `create new merge request` and request your merge with a brief explanation
4. If there are conflicts, **talk to the person you have conflicts with**, and resolve any conflicts in the gitlab UI. (The UI will take you between different places and ask you to choose "ours" or "theirs" in all the conflicts).
5. When done, ask for aproval from a maintainer to merge, you are done.



### Resolving conflicts


If a conflict appears, **talk to the person that did the first commit and figure out whatt should stay or not**.



## One branch, one feature


Each branch must represent **one change or feature, one logical change**. 

To make a new branch that branches from master, 

	git checkout master
	git checkout -b <new-branch-name>
	
_(In a UI, you just say "Create new branch" and it will do it for you)_
	

	
### Naming convention of branches 

Let's try to use a naming convention on the branches that branch from master. The branch should start with one word indicating what *type* of branch is, and then `-` and then a short name of that specific branch.

1. `explore-*` for exploration work
2. `refactor-*` for refactor work
1. `explore-feature-*` Writing new code, a new feature or idea in exploration phase
2. `explore-fix-*` or `explore-bug-*` Fixing a bug of some code in exploration phase
3. `explore-doc-*` Detailing documentation of some code/part of a project in exploration phase
4.  `test-*` Testing something 

## Collaboration in branches that are published to gitlab already


As you are working on the branch, if more than one person want to participate. It is best to **not** use that branch directly. Instead, try to create new branches stemming from that one.

Start those branches with a keyword that describes the branch we are branching from (first letter of each word), and then a descriptive word. 


### Procedure (example)

If two people are working on `feature-googlecloudvisionpdfs`, and we want to write some documentation. 

We can use as keyword `gcv-*` 

```
git checkout feature-googlecloudvision

git checkout -b gcv-pythondoc

```

We would then, write the documentation, and then

```
 git commit -m "Wrote documentaiton of blah blah blah"
 git push -u origin HEAD
```

And create a new merge request form branch `gcv-pythondoc` to `feature-googlecloudvision` in gitlab

(If this branch is going to be used a lot, consider asking to protect the branch, to prevent people from merging directly to this branch in their local machine)

## [Git large file storage](https://about.gitlab.com/2017/01/30/getting-started-with-git-lfs-tutorial/)  
`Large File Storage (LFS)` handles large file for us by saving lightweight pointers in place of real file data. When we checkout a revision with such a pointer, LFS simply looks up the original file and download it for you.  
Because gitlab already supports LFS, we only need to install it in local machine

### Install LFS in local machine
```commandline
pip install git-lfs
git lfs install
``` 
### Procedure
We should tell LFS to track large file as soon as possible, either right after initializing a repo or before adding large file into stage area.
```Python
# Tell LFS to track files with given path
    git lfs track "path_to_large_file"
# Tell LFS to track files with format "*.jpg"
    git lfs track "*.jpg"
# Tell LFS to track content of the whole directory
    git lfs track "data/*"
```
Note: a new file in the project's root folder, `.gitattributes`, will be created to collect all file patterns to track by LFS.  
After telling LFS to track large files, we just do git strategy as normal (even with `.gitattributes` file if there is any changes)