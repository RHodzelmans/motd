from ansible.module_utils.basic import AnsibleModule
from enum import Enum

class State(Enum):
    PRESENT = 1
    ABSENT = 0

class When(Enum):
    BEFORE = 1
    AFTER = 0

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        message=dict(type='str', required=True),
        when=dict(type='enum', required=True),
        state=dict(type='enum', required=False, default=State.PRESENT),
        fqdn=dict(type='bool', required=False, default=False),
        motd=dict(type='str', required=False, default='/etc/motd')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        original_message='',
        new_message='',
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    motd_link = module.params['motd']
    message = module.params['message']

    perform_change(module_args, result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

#
def perform_change(module_args, result):
    input = module_args.params['message']
    result['original_message'] = input
    
    file_loc = module_args.params['motd']
    original_text = read_file()

    if input in original_text:
        result['changed'] = True

        if module_args['when'] = When.BEFORE:
            result['new_message'] = prefix_file(file_loc, input)
        else:
            result['new_message'] = append_file(file_loc, input)
    else: 
        result['new_message'] = 'Same as previous input'
    
# read String message to File at location
def read_file(motd):
    f = open(motd, 'r') 
    read_message = f.read(message)
    f.close()
    return read_message

# append String message to File at location
def append_file(motd, message):
    f = open(motd, 'a') 
    f.write(message)
    f.close

# write String message to File at location before existing content
def prefix_file(motd, message):
    f = open(motd, 'w') 
    original_text = f.read()
    f.write(message + original_text)
    f.close

def main():
    run_module()

if __name__ == '__main__':
    main()