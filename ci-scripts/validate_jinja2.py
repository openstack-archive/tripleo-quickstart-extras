#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2017, Chandan Kumar <chkumar@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from jinja2 import Environment
from jinja2 import exceptions

import io
import os
import sys
import inspect

DOCUMENTATION = '''
---
python script to read and parse jinja2 templates
---
'''

# Jinja Environment
env = Environment()


def get_jinja_files(dir_path):
    """Get all the .j2 and .jinja2 files"""
    files_path = []
    for root, subdir, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.j2') or file.endswith('.jinja2'):
                files_path.append(os.path.join(root, file))

    return files_path


def validate_jinja_templates(file_path):
    """Validate jinja templates file"""
    try:
        with io.open(file_path, 'r', encoding='utf8') as fobj:
            env.parse(fobj.read())
    except exceptions.TemplateSyntaxError as e:
        print('%s has template error: %s' % (file_path, e))
        raise(e)


if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "..")
#    print('base execution directory: %s' % base_dir)
    os.chdir(base_dir)
    jinja_files = get_jinja_files(base_dir)
    for file_path in jinja_files:
        validate_jinja_templates(file_path)
#        print('Validating jinja2: %s' % file_path)
