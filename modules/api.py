from modules.kubeseal import Kubeseal
from flask import request
import json
import logging
from werkzeug.exceptions import *

class API:
    def __init__(self, ks: Kubeseal):
        self.logger = logging.getLogger(__name__)

        # Make Kubeseal available
        self.ks = ks

    def __validate_settings(self, rq: str):
        # Get post body
        settings = json.loads(rq)

        # Check for context in request
        if 'context' not in settings:
            self.logger.warning("Bad request: missing `context` key")
            return False, json.dumps({"error":"missing `context` key"}), 400, {'Content-Type':'application/json'}

        # Check for scope in request
        if 'scope' not in settings:
            self.logger.warning("Bad request: missing `scope` key")
            return False, json.dumps({"error":"missing `scope` key"}), 400, {'Content-Type':'application/json'}

        # check the scope is valid
        validScopes = ['strict', 'namespace-wide', 'cluster-wide']
        if settings['scope'] not in validScopes:
            self.logger.warning("Bad request: invalid scope")
            return False, json.dumps({"error":"invalid scope"}), 400, {'Content-Type':'application/json'}

        # Check for namespace depending of scope
        namespacedScopes = ['strict', 'namespace-wide']
        if settings['scope'] in namespacedScopes:
            if 'namespace' not in settings:
                self.logger.warning("Bad request: missing `namespace` key but request was scoped 'strict' or 'namespace-wide'")
                return False, json.dumps({"error":"missing `namespace` key, required for 'strict' and 'namespace-wide' scopes"}), 400, {'Content-Type':'application/json'}

        # Check for sealed secret name if scope is strict
        if settings['scope'] == "strict" and 'secretName' not in settings:
            self.logger.warning("Bad request: missing `secretName` key but request was scoped 'strict'")
            return False, json.dumps({"error":"missing `secretName` key, required for 'strict' scope"}), 400, {'Content-Type':'application/json'}

        return True, None, None, None


    def __kubesealCheckError(self, sealedSecret):
        # Check for kubeseal error
        if isinstance(sealedSecret, SystemError):
            return False, json.dumps({"error":str(sealedSecret)}), 500, {'Content-Type':'application/json'}

        # Check for other errors
        if isinstance(sealedSecret, LookupError):
            return False, json.dumps({"error":str(sealedSecret)}), 400, {'Content-Type':'application/json'}

        return True, None, None, None


    def sealRaw(self, rq: request):
        postBody = rq.get_json()
        self.logger.debug("New Request: "+str(postBody))

        # Validate request
        status, message, returncode, headers = self.__validate_settings(json.dumps(postBody))
        if not status:
            return message, returncode, headers

        # Validate a value was posted
        if 'value' not in postBody:
            self.logger.warning("Bad request: missing `value` key")
            return json.dumps({"error":"missing `value` key"}), 400, {'Content-Type':'application/json'}

        # Assemble keys into variables
        value = postBody['value']
        context = postBody['context']
        scope = postBody['scope']
        namespace = None if 'namespace' not in postBody else postBody['namespace']
        secretName = None if 'secretName' not in postBody else postBody['secretName']

        # Run Kubeseal
        sealedSecret = self.ks.sealRawValue(value, context, scope, namespace=namespace, secretName=secretName)

        # Check if kubeseal ran successfully
        status, message, returncode, headers = self.__kubesealCheckError(sealedSecret)
        if not status:
            return message, returncode, headers

        # Return the sealed secret
        return json.dumps({"data":sealedSecret}), 200, {'Content-Type':'application/json'}


    def sealFile(self, rq: request):
        # Try to load json
        try:
            postBody = json.loads(rq.form['json'])
        except KeyError:
            self.logger.warning("Bad request: missing `json` form in formdata")
            return json.dumps({"error":"could not get `json` form in formdata"}), 400, {'Content-Type':'application/json'}

        # Validate settings
        status, message, returncode, headers = self.__validate_settings(json.dumps(postBody))
        if not status:
            return message, returncode, headers

        # Validate a file exists
        try:
            file = rq.files['file']
        except BadRequestKeyError:
            self.logger.warning("Bad request: no file found")
            return json.dumps({"error":"missing file"}), 400, {'Content-Type':'application/json'}

        self.logger.debug("New request to seal file: "+str(postBody))
        self.logger.debug("Got file: "+str(rq.files))

        # Assemble keys into variables
        context = postBody['context']
        scope = postBody['scope']
        namespace = None if 'namespace' not in postBody else postBody['namespace']
        secretName = None if 'secretName' not in postBody else postBody['secretName']

        # Run Kubeseal
        sealedSecret = self.ks.sealRawFile(rq.files['file'], context, scope, namespace=namespace, secretName=secretName)

        # Check if kubeseal ran successfully
        status, message, returncode, headers = self.__kubesealCheckError(sealedSecret)
        if not status:
            return message, returncode, headers

        # Return the sealed secret
        return json.dumps({"data": sealedSecret}), 200, {'Content-Type':'application/json'}
