import os
import subprocess
import logging
import yaml
import json

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

class Kubeseal:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)

        # Get config parameters
        self.kubeconfDir = kwargs.get("config_dir", "/kubeconfigs")

        # Set kill
        self.kill = lambda process: process.kill()

        # Get kubeconfig files
        kubeconfFiles = []
        for file in os.listdir(self.kubeconfDir):
            filePath = os.path.join(self.kubeconfDir, file)
            if os.path.isfile(filePath):
                kubeconfFiles.append(os.path.join(self.kubeconfDir, file))
                self.logger.info("Found Kubeconfig at "+os.path.join(self.kubeconfDir, file))
                self.logger.debug(str(open(filePath, "r").read()))

        # Fail if there are no Kubeconfig files
        if len(kubeconfFiles) < 1:
            self.logger.fatal("No Kubeconf Files found!")
            exit(1)

        # Find contexts and create map (context name is key, value is file)
        self.contexts = {}
        for kubeconf in kubeconfFiles:
            file = open(kubeconf, "r")
            kubeconfRaw = yaml.safe_load(file.read())
            for context in kubeconfRaw['contexts']:
                self.contexts[context['name']] = kubeconf
                self.logger.info("Found cluster context \""+str(context['name'])+"\" in \""+str(kubeconf)+"\"")

        # If there are no contexts in any of the files, fail
        if len(self.contexts) < 1:
            self.logger.fatal("Could not find any Kubernetes contexts")
            exit(1)

        # Debug logs
        self.logger.debug("Context Map:\n"+json.dumps(self.contexts, indent=2))


    def getContexts(self):
        return self.contexts


    def sealRawValue(self, value: str, context: str, scope: str, **kwargs):
        # Get kwargs
        namespace = kwargs.get('namespace', None)
        secretName = kwargs.get('secretName', None)

        # Escape single quotes in value
        valueEscaped = str.replace(value, "'", "'\"'\"'")

        # Set default command (for cluster-wide scope only)
        cmd = 'echo -n \''+valueEscaped+'\' | ./bin/kubeseal --raw --scope '+scope+' --kubeconfig '+self.contexts[context]+' --context '+context

        # Update command with namespace if scope is namespace-wide or strict
        if scope in ('namespace-wide','strict'):
            if namespace is None or namespace == "":
                return LookupError("'namespace' key is not defined or is empty")
            cmd = cmd+" --namespace "+namespace

        # Update command if scope is strict
        if scope == "strict":
            if secretName is None or secretName == "":
                return LookupError("'secretName' key is not defined or is empty")
            cmd = cmd+" --name "+secretName

        # Try to run Kubeseal
        try:
            kubeseal = subprocess.run(cmd, shell=True, timeout=10, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            kubesealOut = kubeseal.stdout.decode('utf-8')
            kubesealErr = kubeseal.stderr.decode('utf-8')

            if kubesealErr:
                self.logger.error("Kubeseal encountered an error: "+kubesealErr)
                return SystemError(str(kubesealErr))
        except subprocess.TimeoutExpired as e:
            self.logger.error("Kubeseal timed out...")
            return SystemError(str(e))

        # Return encrypted value
        self.logger.debug("Encrypted new value against context \""+context+"\": "+str(kubesealOut))
        return str(kubesealOut)

    def sealRawFile(self, file: FileStorage, context: str, scope: str, **kwargs):
        # Get kwargs
        namespace = kwargs.get('namespace', None)
        secretName = kwargs.get('secretName', None)

        # Save file to /tmp
        filename = secure_filename(file.filename)
        fileLocation = os.path.join("/tmp", filename)
        file.save(fileLocation)

        # Set default command (for cluster-wide scope only)
        cmd = './bin/kubeseal --raw --from-file '+fileLocation+' --scope '+scope+' --kubeconfig '+self.contexts[context]+' --context '+context

        # Update command with namespace if scope is namespace-wide or strict
        if scope in ('namespace-wide','strict'):
            if namespace is None or namespace == "":
                return LookupError("'namespace' key is not defined or is empty")
            cmd = cmd+" --namespace "+namespace

        # Update command if scope is strict
        if scope == "strict":
            if secretName is None or secretName == "":
                return LookupError("'secretName' key is not defined or is empty")
            cmd = cmd+" --name "+secretName

        # Try to run Kubeseal
        try:
            kubeseal = subprocess.run(cmd, shell=True, timeout=10, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            kubesealOut = kubeseal.stdout.decode('utf-8')
            kubesealErr = kubeseal.stderr.decode('utf-8')

            if kubesealErr:
                self.logger.error("Kubeseal encountered an error: "+kubesealErr)
                return SystemError(str(kubesealErr))
        except subprocess.TimeoutExpired as e:
            self.logger.error("Kubeseal timed out...")
            return SystemError(str(e))

        # Remove file from /tmp
        os.remove(fileLocation)

        # Return encrypted value
        self.logger.debug("Encrypted new file against context \""+context+"\": "+str(kubesealOut))
        return str(kubesealOut)
