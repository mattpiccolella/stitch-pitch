from mongoengine import Document, StringField, FloatField, EmbeddedDocumentListField

class Lyric(Document):
  word = StringField(required=True)
  start_time = FloatField(required=True)
  duration = FloatField(required=True)

class Song(Document):
  title = StringField(required=True)
  file_name = StringField(required=True)
  artist_name = StringField(required=True)
  lyrics = EmbeddedDocumentListField('Lyric')

class VideoClip(Document):
  word = StringField(required=True)
  file_name = StringField(required=True)
  duration = FloatField(required=True)
  author = StringField(required=True)
