import re

from flask import request
from flask_restx import Namespace, fields, Resource
from flask_babel import _

from project.tools import get_short_url, regex, get_short_url_count, get_short_url_popular

shorturl_namespace = Namespace('url', description='request shorturl')

post_request_url = shorturl_namespace.model('Request URL', {
  'url': fields.String(required=True, description='Request url to short')
})

post_answer_url = shorturl_namespace.model('Answer ShortURL', {
  'shortened_url': fields.String(required=True, description='Answered shorturl')
})


class ShortUrl(Resource):
  @shorturl_namespace.marshal_with(post_answer_url)
  @shorturl_namespace.expect(post_request_url, validate=True)
  @shorturl_namespace.response(200, "Success")
  @shorturl_namespace.response(401, "Not found")
  def post(self):
    post_data = request.get_json()
    url = post_data.get("url").strip()

    if re.match(regex, url) is None or not url:
      shorturl_namespace.abort(401, _("Not found"))

    shorturl = get_short_url(url)
    response_object = {
      "shortened_url": request.host_url + shorturl
    }
    return response_object, 200


get_answer_count = shorturl_namespace.model('Answer ShortURL Count', {
  'shortened_url_count': fields.String(required=True, description='Answered shorturl count')
})


class ShortUrlCount(Resource):
  @shorturl_namespace.expect(get_answer_count, validate=False)
  def get(self):
    count = get_short_url_count()
    response_object = {
      "shortened_url_count": str(count)
    }
    return response_object, 200


class ShortUrlPopular(Resource):
  @shorturl_namespace.expect(get_answer_count, validate=False)
  def get(self):
    populars = get_short_url_popular()
    print(populars)
    response_object = {
      "shortened_url_popular": populars
    }
    return response_object, 200


shorturl_namespace.add_resource(ShortUrl, "/shorten")
shorturl_namespace.add_resource(ShortUrlCount, "/count")
shorturl_namespace.add_resource(ShortUrlPopular, "/popular")
