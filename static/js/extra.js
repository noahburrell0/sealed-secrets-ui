//Run initial checks for form
checkScope();
checkMode();

function checkScope(){
    var scope = document.getElementById("scope");
    var scopeValue = scope.options[scope.selectedIndex].value;

    // Div containers
    var namespaceDiv = document.getElementById("namespace");
    var secretNameDiv = document.getElementById("sealed-secret-name");

    // Input Fields
    var namespaceInput = document.getElementById("ns");
    var secretNameInput = document.getElementById("ss-name");

    if(scopeValue == "strict"){
        // Show/Hide Fields
        namespaceDiv.removeAttribute("hidden");
        secretNameDiv.removeAttribute("hidden");
        // Set field requirements
        namespaceInput.setAttribute("required", "");
        secretNameInput.setAttribute("required", "");
    }

    if(scopeValue == "namespace-wide"){
        // Show/Hide Fields
        namespaceDiv.removeAttribute("hidden");
        secretNameDiv.setAttribute("hidden", "");
        // Set field requirements
        namespaceInput.setAttribute("required", "");
        secretNameInput.removeAttribute("required");
    }

    if(scopeValue == "cluster-wide"){
        // Show/Hide Fields
        namespaceDiv.setAttribute("hidden", "");
        secretNameDiv.setAttribute("hidden", "");
        // Set field requirements
        namespaceInput.removeAttribute("required");
        secretNameInput.removeAttribute("required");
    }
}

function checkMode(){
    var mode = document.getElementById("mode");
    var modeValue = mode.options[mode.selectedIndex].value;

    // Div containers
    var uploadDiv = document.getElementById("fileUpload");
    var textarea = document.getElementById("unencryptedTextarea");

    if(modeValue == "file"){
        // Show/Hide Fields
        uploadDiv.removeAttribute("hidden");
        textarea.setAttribute("hidden", "");
    } else {
        // Show/Hide Fields
        uploadDiv.setAttribute("hidden", "");
        textarea.removeAttribute("hidden");
    }

    // When the mode gets set to file, register the element
    file = document.getElementById["unencryptedFile"]
}

function copyToClipboard() {
    // Get the text field
    var copyText = document.getElementById("encrypted");

    // Select the text field
    copyText.select();

     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);

    // Alert the copied text
    UIkit.notification({message: "<div align=\"center\">Copied To Clipboard!</div>", status: 'primary', timeout: 1000});
  }

function encrypt(){
    // Get loading element
    var loading = document.getElementById("loading");

    // Declare uploaded file
    var fileElement = document.getElementById("unencryptedFile")
    var uploadedFile

    // Declare request
    var xhr = new XMLHttpRequest();

    // Get form data
    var data = {
        "context":document.getElementById("context").value,
        "scope":document.getElementById("scope").value,
        "namespace":document.getElementById("ns").value,
        "secretName":document.getElementById("ss-name").value
    };

    // Check the mode to determine if the textfield value should be added to the request
    if ( document.getElementById("mode").value != "file") {
        data.value = document.getElementById("unencrypted").value;
    } else {
        uploadedFile = fileElement.files[0];
    }

    // Prepare request
    xhr.open("POST", "api/seal/"+document.getElementById("mode").value);

    // What to do when server responds
    xhr.onload = function () {
        // Remove loading screen
        loading.classList.add("uk-hidden");

        var returnCode = this.status; // Get return code
        console.log(returnCode);

        // Write encrypted value or return errors as a notification
        if (returnCode == 200){
            var response = JSON.parse(this.response);
            document.getElementById("encrypted").value = response.data;
            document.getElementById("unencrypted").value = "";
        } else if (returnCode == 500) {
            var response = JSON.parse(this.response);
            UIkit.notification({message: response.error, status: 'danger', timeout: 10000});
        } else {
            UIkit.notification({message: '<b><span uk-icon="icon: warning"></span> An unknown error occurred.</b>', status: 'danger', timeout: 10000});
        }
    };

    // Determine if the request should be form-multipart or JSON, and send request - Depends on mode element and API endpoint
    if ( document.getElementById("mode").value == "file") {
        var formData = new FormData();

        // Load form into formdata object as json
        formData.append("json", JSON.stringify(data));

        // Add file to formdata
        formData.append("file", uploadedFile, uploadedFile.name)

        // Send request -- Do not add content type header, fucks with the boundry and causes issues in Flask!
        xhr.send(formData);
    } else {
        // Send request
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(data));
    }

    // Enable loading screen
    loading.classList.remove("uk-hidden");

    // Close all notification while loading
    UIkit.notification.closeAll();


    // Prevent form from reloading page
    return false;
}
