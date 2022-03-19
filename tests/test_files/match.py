link = '<https://example.com/path/>; rel="next"'
match link.split('; '):
    case [brackets_link, 'rel="next"']:
        url = brackets_link[1:-1]
    case [brackets_link, 'rel="previous"']:
        url = brackets_link[1:-1]
    case 'blank':
        url = ''
