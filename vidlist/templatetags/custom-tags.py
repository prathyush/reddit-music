from django import template
import HTMLParser

print "registering template"
register = template.Library()

@register.filter
def decode(value):
	"""HTML decodes a string """
	return  value.decode('string_escape');
