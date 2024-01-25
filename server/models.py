from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

   
    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name field is required.")
        author = db.session.query(Author.id).filter_by(name = name).first()
        # author.query.filter_by(name = name).first()
        if author is not None:
            raise ValueError("Name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        # min post length of 250 chars
        if len(content) < 250:
            raise ValueError("Content must be a minimum of 250 Characters")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        # max post length of 250 chars
        if len(summary) > 250:
            raise ValueError("summary must be a maximum of 250 Characters")
        return summary
    

    @validates('category')
    def validate_category(self, key, category):
        # category is 'Fiction' or 'Non-Fiction' only
        if (category != "Fiction") and (category != 'Non-Fiction'):
            raise ValueError("category must be 'Fiction' or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        # title contains "Won't Believe" "Secret" "Top" or "Guess"
        if not title:
            raise ValueError("title field is required")
        key_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in key_words):
            raise ValueError("title must contain 'Won\'t Believe', 'Secret', 'Top', or 'Guess'" )
        return title
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
