import uuid


def generate_random_id(chars=None, no_special=False, print_id=False):
    ran_id = str(uuid.uuid4())

    if chars:
        try:
            ran_id = ran_id[:chars]
        except Exception as e:
            print(e)

    if no_special:
        ran_id = ran_id.replace("-", "")

    if print_id:
        print("New ID:", ran_id)

    return ran_id
