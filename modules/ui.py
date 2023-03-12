from modules.kubeseal import Kubeseal
from flask import render_template
import logging

class UI:
    def __init__(self, ks: Kubeseal, **kwargs):
        self.logger = logging.getLogger(__name__) 
        # Init self.contexts
        self.contexts = []

        # Convert contexts from dict to list
        contexts = ks.getContexts()
        for context, file in contexts.items():
            self.contexts.append(context)

        # Get UI options        
        self.default_scope = kwargs.get("default_scope", "strict")
        self.scope_tooltip = kwargs.get("scope_tooltip", None)


    def index(self):
        return render_template(
            'index.html.jinja2', 
            scope_tooltip = self.scope_tooltip,
            default_scope = self.default_scope,
            contexts = self.contexts
        )
