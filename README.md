## Hippo

Tool to generate the pip requirements from the packages you *actually* want.

$ pip install -e git+git@github.com:immunda/hippo.git#egg=hippo
$ echo requests > real-requirements.txt
$ hippo generate
$ cat requirements.hippo.txt
