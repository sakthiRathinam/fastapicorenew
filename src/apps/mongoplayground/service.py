def convert_book(obj):
    return {
        "id":str(obj['_id']),
        "title": obj['title'],
        "author_id": obj['author_id'],
        "description": obj['description'],
        "rating": obj['rating'],
    }
