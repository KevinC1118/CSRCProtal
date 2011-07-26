from google.appengine.ext import db


class File(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty(multiline=True)
    creator = db.StringProperty(required=True)
    tags = db.ListProperty(db.Key)
    filename = db.StringProperty()
    space =  db.StringProperty()
    type = db.StringProperty()
    link = db.LinkProperty()
    timestamp = db.DateTimeProperty(required=True)
    
    @property
    def getTags(self):
        return db.get(self.tags)


class Tag(db.Model):
    name = db.StringProperty(required=True)
    
    @property
    def getFiles(self):
        return File.gql('WHERE tag = :1 ORDER BY date DESC', self.key())
