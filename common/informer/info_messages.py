from common.informer import _msg_not_found


def get_msg_not_found_info() -> str:
    return _msg_not_found


def get_ignore_msg_info() -> str:
    return 'Message was ignored'
    # return (f'{get_detected_message_url('Message')} from {get_user_name()} was '
    #         f'{markdown.hunderline('ignored')}\n\n{get_detected_message_quote()}')


def get_delete_msg_info() -> str:
    return 'Message was deleted'
    # return (f'Message from {get_user_name()} was {markdown.hunderline('deleted')}\n\n'
    #         f'{get_detected_message_quote()}')


def get_mute_user_info() -> str:
    return 'User was muted'
    # return f'{get_user_name()} was {markdown.hunderline('muted')}\n\n{get_detected_message_quote()}'


def get_ban_user_info() -> str:
    return 'User was banned'
    # return f'{get_user_name()} was {markdown.hunderline('banned')}\n\n{get_detected_message_quote()}'


def get_info_for_admins() -> str:
    return 'Suspicious message was detected'
    # return (f'{get_user_name()} says {get_detected_message_url('bad words')}\n\n'
    #         f'{get_detected_message_quote()}')
