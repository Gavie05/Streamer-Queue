# Return required base64 string for the "Authorization" Header using the client id and client secret
def auth_encode(client_id, client_secret):
    import base64

    #Combine client id and client secret into required format and encode
    joined_string = client_id + ':' + client_secret
    joined_bytes = joined_string.encode('ascii')
    
    # Decode into ascii string
    base64_bytes = base64.b64encode(joined_bytes)
    base64_string = base64_bytes.decode('ascii')
    
    return base64_string