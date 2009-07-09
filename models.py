import random
import datetime

from google.appengine.ext import db
from google.appengine.ext import search

class SchoolImport(search.SearchableModel):
	urn = db.IntegerProperty()
	local_authority_id = db.IntegerProperty()
	local_authority_name = db.StringProperty()
	estab = db.IntegerProperty()
	school_name = db.StringProperty()
	street = db.StringProperty()
	locality = db.StringProperty()
	address_3 = db.StringProperty()
	town = db.StringProperty()
	county = db.StringProperty()
	postcode = db.StringProperty()
	telephone_std = db.StringProperty()
	telephone_number = db.StringProperty()
	head_title = db.StringProperty()
	head_first_name = db.StringProperty()
	head_last_name = db.StringProperty()
	head_honours = db.StringProperty()
	establishment_type = db.StringProperty()
	education_phase = db.StringProperty()
	statutory_lowest_age = db.IntegerProperty()
	statutory_highest_age = db.IntegerProperty()


# elements for sharded counter
	
class CounterConfig(db.Model):
	name = db.StringProperty(required=True)
	num_shards = db.IntegerProperty(required=True, default=1)

class Counter(db.Model):
	name = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True, default=0)


def get_counter(name):
	total = 0
	for counter in Counter.gql('WHERE name = :1', name):
		total += counter.count
	return total


def increment_counter(name):
	config = CounterConfig.get_or_insert(name, name=name)
	def txn():
		index = random.randint(0, config.num_shards - 1)
		shard_name = name + str(index)
		counter = Counter.get_by_key_name(shard_name)
		if counter is None:
			counter = Counter(key_name=shard_name, name=name)
		counter.count += 1
		counter.put()
	db.run_in_transaction(txn)

