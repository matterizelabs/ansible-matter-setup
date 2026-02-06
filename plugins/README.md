# Custom Modules

Place custom Ansible modules in `plugins/modules/`.

Example skeleton:

```python
#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        )
    )

    name = module.params['name']

    module.exit_json(changed=False, name=name)

if __name__ == '__main__':
    main()
```

Then call it in a playbook:

```yaml
- name: Example custom module usage
  my_custom_module:
    name: "example"
```
