from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    description = fields.Str(validate=validate.Length(min=0, max=200), missing='')
    priority = fields.Str(validate=validate.OneOf(['LOW', 'MEDIUM', 'HIGH']), missing='MEDIUM')
    state = fields.Str(validate=validate.OneOf(['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']), missing='PENDING')
    expiration_date = fields.DateTime(allow_none=True)
    creation_date = fields.DateTime(dump_only=True)

class TaskUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=80))
    description = fields.Str(validate=validate.Length(min=1, max=200))
    priority = fields.Str(validate=validate.OneOf(['LOW', 'MEDIUM', 'HIGH']))
    state = fields.Str(validate=validate.OneOf(['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']))
    expiration_date = fields.DateTime(allow_none=True)