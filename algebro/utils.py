def id_from_mention(mention):
    return mention.replace('<', '').replace('>', '').replace('@', '').replace('!', '')
