from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search

import models


class SchoolLoader(bulkload.Loader):
  def __init__(self):
    bulkload.Loader.__init__(self, 'SchoolImport',
                         [
						("urn", int),
						("local_authority_id", int),
						("local_authority_name", str),
						("estab", int),
						("school_name", str),
						("street", str),
						("locality", str),
						("address_3", str),
						("town", str),
						("county", str),
						("postcode", str),
						("telephone_std", str),
						("telephone_number", str),
						("head_title", str),
						("head_first_name", str),
						("head_last_name", str),
						("head_honours", str),
						("establishment_type", str),
						("education_phase", str),
						("statutory_lowest_age", int),
						("statutory_highest_age", int),
                          ])

  def HandleEntity(self, entity):
    ent = search.SearchableEntity(entity)
    models.increment_counter("school_total")
    return ent

if __name__ == '__main__':
  bulkload.main(SchoolLoader())