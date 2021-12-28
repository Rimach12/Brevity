import os, secrets
from flask import current_app
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError, StopValidation

from collections import Iterable
from werkzeug.datastructures import FileStorage

from brevity.models import Downvote, Post, Upvote, User
from brevity import db

def save_file(form_file):
    random_hex = secrets.token_hex(8)                                           # To randomize the name of the uploaded image so that the name doesn't collide with the already uploaded ones 
    _, f_ext = os.path.splitext(secure_filename(form_file.filename))            # Splits the filename and extension in 2 part.
                                            # We don't need the filename. That's why we represent it with '_'.
                                            #     To let the editor know that it's unused.
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static', 'resource_files', file_fn )
    
    form_file.stream.seek(0)
    form_file.save(file_path)
    form_file.close()

    return file_fn


def delete_file(filename):
    file_to_delete = os.path.join(current_app.root_path,'static','resource_files', filename)   
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
    return


def FileSizeLimit(max_size_in_mb):
        max_bytes = max_size_in_mb*1024*1024
        def file_length_check(form, field):
            for file in field.data: 
                if len(file.read()) > max_bytes:
                    raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
        
        return file_length_check

        

class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):

        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            if not data:
                return 
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                print(filename, flush=True)
                print(any(filename.endswith("." + x) for x in self.upload_set), flush=True)
                if not any(filename.endswith("." + x) for x in self.upload_set):
                    raise StopValidation(
                        self.message
                        or field.gettext("File does not have an approved extension: {extensions}").format(
                            extensions=", ".join(self.upload_set)
                        )
                    )

def getTagData(post):
    tagData = ''
    for tag in post.tags:
        tagData += tag.tag
        tagData += ','
    sz = len(tagData)
    tagData = tagData[:sz-1]
    return tagData


def calculateContribution(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    totalUpvote = db.session.query(User).join(Post).join(Upvote).filter(User.id==Post.user_id).filter(Post.id==Upvote.post_id).filter(User.id==post.user_id).with_entities(Upvote.user_id).count()
    impactOfUpvote = totalUpvote*int(os.getenv('impactOfUpvote'))

    totalDownvote = db.session.query(User).join(Post).join(Downvote).filter(User.id==Post.user_id).filter(Post.id==Downvote.post_id).filter(User.id==post.user_id).with_entities(Downvote.user_id).count()
    impactOfDownvote = totalDownvote*int(os.getenv('impactOfDownvote'))

    contribution = impactOfUpvote-impactOfDownvote
    return contribution
                                                                 
                                                                                                                                                                                                             

                                                                                                                                                                                                             