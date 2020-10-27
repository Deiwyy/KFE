# KFE
Kapa File Explorer

A simple file explorer with basic functions. Project made mainly for fun, I work on it when i feel kinda bored. 
I don't want to release it as an official piece of software by any means.

As for now, you can create new files, copy, delete and move files or directories. 
You can also kinda customize the program, just change what I call 'texts' in the txts.txt file (1.1.2 only). 

The syntax for these texts goes like this 

```
-[name of the key]
some text
you can use multiline too
=
```

With '-' meaning the start of a text, the string directly behind the '-' will be the name of the text, which will be a key in `texts` dictionary in the code.
The '=' means the end of the texts.

Everything after a '=' and not after a '-' will not count which means you can have anything writen in between the texts. For example you can use it to comment on your texts:

```
use when the user does not have a permission to read or write to a file
-noPermission
Seems like you don't have the permission to perform this operation on this file/directory
=

I just like having random stuff in between my texts, this line here won't count

-doesNotExist
Seems like the file/dir you are trying to perform an action on doesn't exist
=

This one will neither count

-sometext
But this will, this whole text will be stored in the texts dictionary under the key 'sometext'

so texts['sometext']

=
```
