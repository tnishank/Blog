from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField, TextAreaField, \
    BooleanField
from wtforms.validators import Required,Length, Email, Regexp
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

#This form is used to edit the profile of user
class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    location = StringField('Location', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

#This form is used to edit the profile of admin
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    #username should be of length from 1 to 64
    #It can have alphabets numbers _ and . But should start from alphabets 
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    
    #coerce=int argument is added to store field as integers 
    #instead of the default, which is strings.
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user
    #Validates email during editing
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    #Validates user name during editing
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
            
#Form for The Post
class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

#Form for comment
class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')