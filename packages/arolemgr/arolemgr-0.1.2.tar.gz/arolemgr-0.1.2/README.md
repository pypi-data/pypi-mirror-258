# arolemgr
[arolemgr](https://github.com/MichaelRoosz/arolemgr) is a fork of the [ansible-galaxy](https://github.com/ansible/ansible) cli tool enhanced with additional features.

# Additional Features
- support for concurrent role downloads via the `--max-concurrent-downloads` option

# Usage
arolemgr can be used as a drop-in replacement for `ansible-galaxy`, see https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html for a list of available commands.

Additionally, these features are available:

## role install
- the `--max-concurrent-downloads` option has been added to allow downloading multiple roles in parallel, its default value is `3`.
  example usage:
  ```
  arolemgr role install -p roles -r requirements.yml --max-concurrent-downloads 10
  ```
