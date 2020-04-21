# INI File Merger - Ansible Module

Takes two INI files a *source* and *target* and merges all of *source*'s
sections and keys into *target* file.

## Installing
Copy `ini_merge.py` to `roles/ironsigma_modules/library` in your playbook directory.

## Usage In Playbook
Include the module role before you use it:

```yml
---
- hosts: webservers
  roles:
    - ironsigma_modules
    - some_other_role_using_ini_module
```

## Usage In Roles

The following will read *my_settings.ini* and apply them to */etc/global.ini*.

```yml
---
- name: Merge settings
  ini_merge:
    source: my_settings.ini
    target: /etc/global.ini
```

Optionally you can specify `overwrite_values: no` to prevent from modifying
*global.ini* values already there, and only applying any missing ones.

Setting `no_extra_spaces: yes` will output the key value pairs as `key=value`
instead of spacing them out as `key = value`. Note this will only work under Python 3.