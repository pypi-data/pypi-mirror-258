from fumedev.index.Documentation import Documentation

def search_snippet(query, extension='', file_path=''):
    doc = Documentation()
    snip_lst = doc.search_code(query=query, extension=extension, file_path=file_path, k=2)
    return snip_lst, [snip.get('file_path') for snip in snip_lst]



