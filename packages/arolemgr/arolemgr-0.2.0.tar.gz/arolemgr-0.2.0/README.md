# arolemgr
[arolemgr](https://github.com/MichaelRoosz/arolemgr) is a fork of the [ansible-galaxy](https://github.com/ansible/ansible) cli tool enhanced with additional features.

# Additional Features
- support for concurrent role downloads via the `--max-concurrent-downloads` option
- support for http authentication

# Usage
arolemgr can be used as a drop-in replacement for `ansible-galaxy`, see https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html for a list of available commands.

Additionally, these features are available:

## role install
- the `--max-concurrent-downloads` option has been added to allow downloading multiple roles in parallel, its default value is `3`.
  example usage:
  ```
  arolemgr role install -p roles -r requirements.yml --max-concurrent-downloads 10
  ```

- the 'src' attribute has been extended to allow http authentication for http urls.
  example usage:
  ```
  - name: role1
    src: auth:bb_cloud:https://bitbucket.org/user/role1/get/v1.0.0.tar.gz
    version: v1.0.0
  ```
  username and password will now be read from the environment variables 'ANISBLE_GALAXY_AUTH_BB_CLOUD_USERNAME' and 'ANISBLE_GALAXY_AUTH_BB_CLOUD_PASSWORD' (the environment variable names must be all uppercase).
