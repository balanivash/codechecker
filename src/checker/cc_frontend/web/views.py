from django.template import RequestContext
from django.conf import settings
import django.shortcuts
import datetime, sys

# This is a wrapper function to render_to_response which will have global variables that needs to be
# passed along with other context variables. Request Context is also passed here
# This should ideally become a decorator for RequestContext. Will have to fix it as soon as I found it how.
def render_to_response( request, *args, **kwargs ):
    #our custom dictionary with additional Parameters
    template = args[0]
    vars = args[1]
    
    #passing the request Context
    kwargs['context_instance'] = RequestContext( request )
    vars['stylesheet'] = settings.STYLESHEET + '.html'
    vars['media_url_prefix'] = settings.MEDIA_URL[:-1]
    vars['prefix'] = settings.BASE_URL[:-1]
    
    return django.shortcuts.render_to_response( template, vars, **kwargs )

# Load the default Home page, About page, References page and a sample view
def default( request, action = 'default' ):  
    template = action + '.html'
    vars = {}
    return render_to_response( request, template, vars )


