#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import shutil

class ParserError(Exception):
    pass


def usage():
    print("usage: inject_log.py [OPTION] [PATH]")
    print("options:")
    print("-c \t create InjectLog.smali in apktool project root directory")
    print("-r \t recursive inject")
    print("-h \t help\n")
    print("example:")
    print("inject_log.py -c ./")
    print("create InjectLog.smali, if current working directory is apktool project root directory\n")
    print("inject_log.py -c c:\\project")
    print("create InjectLog.smali, if c:\\project is apktool project root directory\n")
    print("inject_log.py ./")
    print("inject log into all smali file under current working directory\n")
    print("inject_log.py -r ./")
    print("inject log into all smali file under current working directory and subdirectory recursively\n")
    print("inject_log.py c:\\project\\alipay.smali")
    print("inject log into alipay.smali\n")
    print("inject_log.py c:\\project")
    print("inject log into all smali file under c:\\project\n")
    print("inject_log.py -r c:\\project")
    print("inject log into all smali file under c:\\project and subdirectory recursively\n")


# 注入代码到一个行数块中
def inject_code_to_method_section(method_section):

    # 对象的构造函数，是否插入日志？默认插入，如果不插，取消注释
    #if method_section[0].find("constructor <init>") != -1:
    #    return method_section

    # 静态构造函数，无需处理
    if method_section[0].find("static constructor") != -1:
        return method_section
    # synthetic函数，无需处理
    if method_section[0].find("synthetic") != -1:
        return method_section
    # 抽象方法，无需处理
    if method_section[0].find("abstract") != -1:
        return method_section
    # native方法，不处理
    if method_section[0].find("native") != -1:
        return method_section
    # 超短方法，不注入
    if len(method_section) < 3:
        return method_section
    # 已经注入过，不重复注入
    if "Lcom/hook/tools/InjectLog;->PrintCaller()V" in method_section[2]:
        return method_section
    # 生成待插入代码行
    code = [
        '\n',
        '    invoke-static {}, Lcom/hook/tools/InjectLog;->PrintCaller()V\n',
        '\n'
    ]
    # 插入到.method的下一行
    method_section[1:1] = code
    return method_section


# 注入代码到一个smali文件中
def inject_code_to_smali_file(smali_file_path):
    print("Inject: {0}".format(smali_file_path))
    with open(smali_file_path, "r", encoding = "utf-8") as file:
        old_content = file.readlines()
        file.close()

    new_content = []
    method_section = []
    method_begin = False
    for line in old_content:
        if line[:7] == ".method":
            method_begin = True
            method_section.append(line)
            continue
        if method_begin:
            method_section.append(line)
        else:
            new_content.append(line)
        if line[:11] == ".end method":
            if not method_begin:
                # 奇葩 .method 和 .end method 不成对出现
                raise ParserError("asymmetric .method")
            method_begin = False
            method_section = inject_code_to_method_section(method_section)
            new_content.extend(method_section)
            method_section.clear()

    with open(smali_file_path, "w", encoding="utf-8") as file:
        file.writelines(new_content)
        file.close()


def create_injectlog_smali_file(apktool_project_path):
    target_path = os.path.join(apktool_project_path, "smali")
    if not os.path.exists(target_path):
        raise Exception("not find 'smali' directory in apktool project root directory: " + apktool_project_path)
    target_path = os.path.join(target_path, "com/hook/tools/")
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    target_path = os.path.join(target_path, "InjectLog.smali")
    source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "InjectLog.smali")
    shutil.copy(source_path, target_path)
    print("create InjectLog.smali ok: " + target_path)


def inject_log(path, is_recursion = False):
    if not os.path.exists(path):
        raise Exception("path not exists: " + path)
    if os.path.isfile(path):
        inject_code_to_smali_file(path)
    elif os.path.isdir(path):
        if is_recursion:
            walker = os.walk(path)
            for root, directory, files in walker:
                for file_name in files:
                    if file_name[-6:] != ".smali":
                        continue
                    smali_file_path = os.path.join(root, file_name)
                    inject_code_to_smali_file(smali_file_path)
        else:
            files = os.listdir(path)
            for file_name in files:
                if file_name[-6:] != ".smali":
                    continue
                smali_file_path = os.path.join(path, file_name)
                inject_code_to_smali_file(smali_file_path)

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h":
            usage()
        else:
            inject_log(sys.argv[1])
        return
    if len(sys.argv) == 3:
        if sys.argv[1] == "-c":
            create_injectlog_smali_file(sys.argv[2])
            return
        elif sys.argv[1] == "-r":
            inject_log(sys.argv[2], is_recursion = True)
            return
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-c":
            create_injectlog_smali_file(sys.argv[2])
            return
    usage()


if __name__ == '__main__':
    main()



