# copy-to

A little python script i use in conjunction with git so you can easily copy config files from anywhere in an instant to do whatever with!

Depends on [argcomplete](https://pypi.org/project/argcomplete/)

Install it with:

```
pipx install copy-to
```
Try running it once if autocompletions aren't working

``` 
sudo activate-global-python-argcomplete
```
for installing pythoncompletions globally.

Add a pairset of destination folder - source files and/or directories with 
```
copy-to add myname destination_folder sourcefile1 (sourcefolder1 sourcefile2 sourcefile3 sourcefolder2/*) ...
```

List configured paths and files with 
```
copy-to list myname
``` 
or just 
```
copy-to list
```
You can also use 'all' to list/run all regular names 


Copy the files to their destination by running 
```
copy-to run myname1 (myname2)
```

Or copy the files back to source by running 
```
copy-to run-reverse myname1 (myname2)
```

Delete set of dest/src by name with 
```
copy-to delete myname1 (myname2)
```

Add sources with 
```
copy-to add_source myname folder1 file1
```

Delete source by index with
```
copy-to delete_source myname 1 4 7
```

Reset source and destination folders
```
copy-to reset_source myname
copy-to reset_destination myname newDest
```

Groups are based on names. For copying to multiple directories in one go.
Takes up 'group' as config namespace.

Add groupname
```
copy-to add_group mygroupname myname1 myname2
```

Delete groupname
```
copy-to delete_group mygroupname
```

Configuration files at `~/.config/copy-to/confs.json` for Linux 

Windows and mac not tested
