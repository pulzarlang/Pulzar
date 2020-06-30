def POST(value, post_requests):
    for i in post_requests:
        if i[0] == value:
            return i[1]

def GET(value, get_requests):
    for i in get_requests:
        if i == value:
            return get_requests[i][0]