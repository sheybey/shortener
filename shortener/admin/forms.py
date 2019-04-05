from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class LinkForm(FlaskForm):
    key = StringField(
        'Key',
        validators=[
            DataRequired(message='Missing key'),
            Length(
                message='Key must be %(max)d characters or less',
                max=128
            )
        ]
    )
    target = StringField(
        'Target',
        validators=[
            DataRequired(message='Missing target'),
            Length(
                message='Target must be %(max)d characters or less',
                max=1024
            )
        ]
    )


class DeleteLinkForm(FlaskForm):
    # I'm kind of cheating here to get free CSRF protection without forcing it
    # on every view of the containing app. There's probably a better way of
    # doing this...
    pass
