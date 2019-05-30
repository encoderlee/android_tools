### what
reverse analysis an android app
use apktool unpack apk
use this script inject log to smali file automatically
use apktool rebuild apk
then logcat will show us the invoked process of each function
### step
1. use apktool unpack apk
2. run inject_log.py -c [apktool project root directory]
3. run inject_log.pt -r [the directory of interested java package]
4. apktool rebuild apk
5. run apk, watch logcat with tag 'InjectLog'

### example
inject_log.py -c ./
create InjectLog.smali, if current working directory is apktool project root directory

inject_log.py -c c:\project
create InjectLog.smali, if c:\project is apktool project root directory

inject_log.py ./
inject log into all smali file under current working directory

inject_log.py -r ./
inject log into all smali file under current working directory and subdirectory recursively

inject_log.py c:\project\alipay.smali
inject log into alipay.smali

inject_log.py c:\project
inject log into all smali file under c:\project

inject_log.py -r c:\project
inject log into all smali file under c:\project and subdirectory recursively

### detail
[https://blog.csdn.net/CharlesSimonyi/article/details/90691417](https://blog.csdn.net/CharlesSimonyi/article/details/90691417)