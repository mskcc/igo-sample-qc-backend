import datetime

class Comment(db.Model):
	"""
	Create a Comment table
	"""

	__tablename__ = 'comments'
	# __table_args__ = ??

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), db.ForeignKey('users.username'), nullable=False)
	user_title = db.Column(db.String(60), nullable=False)
	comment = db.Column(db.Text(), nullable=False)
	request_id = db.Column(db.String(40), nullable=False)
	qc_table = db.Column(db.String(40), nullable=False)
	date_created = db.Column(db.datetime, nullable=False)
	date_updated = db.Column(db.datetime, nullable=True)
	
	def __init__(
	self,
	username,
	user_title,
	comment,
	request_id,
	qc_table,
	date_created=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	date_updated
	):

	self.username = username
	self.user_title = user_title
	self.comment = comment
	self.request_id = request_id
	self.qc_table = qc_table
	self.date_created = date_created
	self.date_updated = date_updated