from src.schemas import CommentSchema, PostSchema, UserSchema

def _clean_str(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None

def transform_user(user: UserSchema) -> dict:
    return {
        "id": user.id,
        "name":_clean_str(user.name),
        "username":_clean_str(user.username),
        "email":user.email.lower().strip(),
        "phone": _clean_str(user.phone),
        "website": _clean_str(user.website),
        "company_name": _clean_str(user.company.name),
        "company_catch_phrase": _clean_str(user.company.catchPhrase),
        "company_bs": _clean_str(user.company.bs) 
    }

def transform_address(user: UserSchema) -> dict:
    addr = user.address
    return {
        "user_id": user.id,
        "street": _clean_str(addr.street),
        "suite": _clean_str(addr.suite),
        "city": _clean_str(addr.city),
        "zipcode": _clean_str(addr.zipcode),
        "geo_lat": float(addr.geo.lat),
        "geo_lng": float(addr.geo.lng),
    }


def transform_post(post: PostSchema) -> dict:
    return {
        "id": post.id,
        "user_id": post.userId,
        "title": _clean_str(post.title),
        "body": (post.body or "").strip(),
    }


def transform_comment(comment: CommentSchema) -> dict:
    return {
        "id": comment.id,
        "post_id": comment.postId,
        "name": _clean_str(comment.name),
        "email": comment.email.lower().strip(),
        "body": (comment.body or "").strip(),
    }