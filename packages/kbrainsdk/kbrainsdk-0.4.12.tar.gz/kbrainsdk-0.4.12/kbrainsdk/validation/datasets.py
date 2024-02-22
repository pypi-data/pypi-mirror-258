from kbrainsdk.validation.common import get_payload, validate_email

def validate_list_datasets(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    search_term = body.get('search_term')

    focus_chat_id = None
    if "focus_chat_id" in body:
        focus_chat_id = body.get('focus_chat_id')

    selected_datasets = None
    if body.get('selected_datasets'):
        selected_datasets = body.get('selected_datasets')
        if selected_datasets == []:
            selected_datasets = None


    # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting email, token, client_id, oauth_secret, tenant_id")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id, selected_datasets, search_term, focus_chat_id

def validate_search_datasets(req):
    body = get_payload(req)
    query = body.get('query')
    topic = body.get('topic')
    citations = body.get('citations')

    # Validate parameters
    if not all([query, topic, citations]):
        raise ValueError("Missing or empty parameter in request body. Expecting query, topic, citations")

    if not isinstance(citations, int):
        raise ValueError("Citations must be an integer")

    return query, topic, citations

def validate_list_dataset_files(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    dataset_id = body.get('dataset_id')
    pagination = None
    search_term = None
    if "search_term" in body:
        search_term = body.get('search_term')

    if "pagination" in body:
        pagination = body.get('pagination')
    
    max_item_count = 10
    if "max_item_count" in body:
        max_item_count = body.get('max_item_count')

    # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id, dataset_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting email, token, client_id, oauth_secret, tenant_id, dataset_id")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id, dataset_id, pagination, max_item_count, search_term

def validate_list_focus_configurations(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    search_term = None
    if search_term in body:
        search_term = body.get('search_term')

    # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting email, token, client_id, oauth_secret, tenant_id")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id, search_term    