# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
diff common api
diff 相关共通函数
"""

import difflib
import json
import os

from common import logcm
from common import filecm
from common import strcm
from filecmp import dircmp


def diff_by_lines(lines1, lines2):
    """
    比较两个字符串列表。
    @param lines1: 字符串列表1
    @param lines2: 字符串列表2
    @return: None
    """

    # differ对象
    differ = difflib.Differ()
    # 比较处理
    diff = differ.compare(lines1, lines2)
    # 转成字符串列表
    diff_list = list(diff)

    # 左侧行号
    line_left = 0
    # 右侧行号
    line_right = 0
    # 行循环
    for i in range(len(diff_list)):
        # 行内容
        line = diff_list[i]

        if line.startswith("-"):
            # 左侧文本打印
            line_num_str = '[%d]' % line_left
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='green', bg='black')
            # 左侧行号+1
            line_left += 1
        elif line.startswith("+"):
            # 右侧文本打印
            line_num_str = '[%d]' % line_right
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='orange', bg='black')
            # 右侧行号+1
            line_right += 1
        elif line.startswith("?"):
            # 不同点标注
            logcm.print_style('%s %s' % (' ' * len(line_num_str), line[2:]), fg='red', bg='black', end='')
        else:
            # 相同内容行
            logcm.print_style('[%d] %s' % (line_left, line[2:]), color='disable', fg='black', bg='lightgrey')
            logcm.print_style('[%d] %s' % (line_right, line[2:]), color='disable', fg='black', bg='lightgrey')
            # 左右侧行号+1
            line_left += 1
            line_right += 1


def diff_by_text(text1, text2):
    """
    比较两个文本。
    @param text1: 文本1
    @param text2: 文本2
    @return: None
    """

    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()
    logcm.print_info("diff_by_text text1[%d] vs text2[%d]" % (len(text1_lines), len(text2_lines)))
    diff_by_lines(text1_lines, text2_lines)


def diff_by_dict(dict1, dict2):
    """
    比较两个字典。
    @param dict1: 字典1
    @param dict2: 字典2
    @return: None
    """

    json1 = json.dumps(dict1, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    json2 = json.dumps(dict2, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    diff_by_text(json1, json2)


def diff_by_file(file_path1, file_path2, encoding='utf-8'):
    """
    比较两个文本文件。
    @param file_path1: 文件路径1
    @param file_path2: 文件路径2
    @param encoding: 文本编码
    @return: None
    """

    logcm.print_info("diff_by_file file1[%s] vs file2[%s]" % (file_path1, file_path2))
    lines1 = filecm.read_lines(file_name=file_path1, encoding=encoding)
    lines2 = filecm.read_lines(file_name=file_path2, encoding=encoding)
    diff_by_lines(lines1, lines2)


def diff_by_dir(dir_path1, dir_path2, dcmp=None, column_size=80):
    """
    比较两个目录。
    @param dir_path1: 文件目录1
    @param dir_path2: 文件目录2
    @param dcmp: 目录比较结果对象，为空则执行首层目录比较
    @param column_size: 打印列宽度，用于补空对齐
    @return: None
    """

    if dcmp is None:
        logcm.print_info("diff_by_dir dir1[%s] vs dir2[%s]" % (dir_path1, dir_path2))
        dcmp = dircmp(dir_path1, dir_path2)
        diff_by_dir(dir_path1, dir_path2, dcmp, column_size)
    else:
        # 取得左右合集，去重，并排序
        all_list = list(set(dcmp.left_list + dcmp.right_list))
        all_list.sort()
        empty_file = ' ' * column_size
        for file_name in all_list:
            # 显示的文件名
            left_file = os.path.join(dir_path1, file_name)
            right_file = os.path.join(dir_path2, file_name)
            # 打印控制
            if file_name in dcmp.left_only:
                logcm.print_style('%s %s' % (left_file, empty_file), fg='green', bg='black')
            elif file_name in dcmp.right_only:
                logcm.print_style('%s %s' % (empty_file, right_file), fg='green', bg='black')
            elif file_name in dcmp.diff_files:
                logcm.print_style(
                    '%s %s' % (strcm.pad_after(left_file, column_size), right_file),
                    fg='red', bg='black')
            elif file_name in dcmp.same_files:
                logcm.print_style(
                    '%s %s' % (strcm.pad_after(left_file, column_size), right_file),
                    color='disable', fg='black', bg='lightgrey')

        # 子目录递归
        for sub_dcmp in dcmp.subdirs.values():
            diff_by_dir(sub_dcmp.left, sub_dcmp.right, sub_dcmp, column_size)
