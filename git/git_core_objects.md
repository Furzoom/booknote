# Git core objects

## Core objects in git

 - blob object
 - tree object
 - commit object

## Git low level commands

 - git hash-object
 - git cat-file
 - git update-index
 - git write-tree
 - git read-tree
 - git commit-tree

### git hash-object

`git hash-object` used to compute object ID and optionally create a blob from a file.

```shell
$ echo "Hello furzoom" | git hash-object -w --stdin
85b75207c07fe1be1e5116f73b74e1eb4a92a4a5
```

`-w` tells hash-object to store the object. `--stdin` tells the command to read the content from stdin.

### git cat-file

`git cat-file` provide content or type and size information for repository objects.

```shell
$ git cat-file -p 85b75207c07fe1be1e5116f73b74e1eb4a92a4a5
Hello furzoom
```

`p` tells cat-file to figure out the type of content and display it nicely for you.

### git update-index

`git update-index` register file contents in the working tree to the index.

```shell
$ echo 'new file' > new.txt
$ git update-index --add new.txt
```

`--add` tells update-index to add file to index (staging area).

### git write-tree

`git write-tree` create a tree object from the current index.

```shell
$ git write-tree
```

### git read-tree

`git read-tree` reads tree information into the index.

```shell
$ git read-tree <tree-sha1>
```

### git commit-tree

`git commit-tree` create a new commit object.

```shell
$ git commit-tree <tree-sha1> -p <parent-tree-sha1>
```


[Three core objects in git](https://www.git-scm.com/book/en/v2/Git-Internals-Git-Objects)
