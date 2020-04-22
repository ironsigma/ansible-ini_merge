#!/usr/bin/python

# Copyright: (c) 2020, Juan D Frias <juandfrias@gmail.com>
# MIT License see LICENSE file for details

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['stableinterface'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: ini_merge

short_description: Merge an existing INI file with another.

version_added: "2.5.1"

description:
    - "This module will take an existing INI file and read all sections and keys and merge with another INI fle."

options:
    source:
        description:
            - File to use as patch
        required: true
    target:
        description:
            - File merge source with
        required: true
    overwrite_values:
        description:
            - Do not ovewrite existing values
        default: true
        required: false
    no_extra_spaces:
        description:
            - Do not insert spaces before or after the '=' symbol (python3 only)
        default: false
        required: false

author:
    - Juan D Frias (@ironsigma)
'''

EXAMPLES = '''
# Merge INI files
- name: Merge settings
  ini_merge:
    source: "{{ role_path }}/files/my_settings.ini"
    target: global.ini
'''

import sys
import os

from ansible.module_utils.basic import AnsibleModule

py3 = sys.version_info > (3, 0)

if py3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


def run_module():
    module_args = dict(
        source=dict(type='path', required=True),
        target=dict(type='path', required=True),
        overwrite_values=dict(type='bool', required=False, default=True),
        no_extra_spaces=dict(type='bool', required=False, default=False),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Check if source is found
    if not os.path.exists(module.params['source']):
        module.fail_json(msg='Source file does not exist.', **result)

    # Load source file
    source_ini = ConfigParser(allow_no_value=True)
    source_ini.read(module.params['source'])

    # Load target file
    target_ini = ConfigParser(allow_no_value=True)
    target_ini.read(module.params['target'])

    # Merge files
    for section in source_ini.sections():
        if not target_ini.has_section(section):
            result['changed'] = True
            target_ini.add_section(section)

        for (option, value) in source_ini.items(section):
            if not module.params['overwrite_values'] and target_ini.has_option(section, option):
                continue

            result['changed'] = True
            target_ini.set(section, option, value)

    # Handle no extra spaces
    write_options = {}
    if py3:
        write_options['space_around_delimiters'] = not module.params['no_extra_spaces']

    # Write out the merged file
    if not module.check_mode and result['changed']:
        with open(module.params['target'], 'w') as target_file:
            target_ini.write(target_file, **write_options)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
