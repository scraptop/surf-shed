# Prepare your machine

Have ansible installed on your machine (Not needed on the server)

```
apt install ansible
```

Install dependencies

```
ansible-galaxy collection install ansible.posix
```

# Test that ansible works:

```
ansible all -i inventory  -m ping -vvv
```


# Run playbooks

## Add user

```
ansible-playbook playbooks/add-user.yaml -i inventory
```

```
ansible-playbook playbooks/add-auth-keys.yaml -i inventory
```