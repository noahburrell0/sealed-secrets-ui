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
            line_counter(); // Reset line counter

            // Set filename based on mode when we get a 200 back
            setFilename(document.getElementById("mode").value, uploadedFile);
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

// Add line numbers to unencrypted text area
// declare elements
var codeEditor = document.getElementById('unencrypted');
var lineCounter = document.getElementById('lineCounter');
var codeEditorJQ = $("#unencrypted");
var lineCounterJQ = $("#lineCounter");

// Scroll with the unencrypted textarea
codeEditor.addEventListener('scroll', () => {
    lineCounter.scrollTop = codeEditor.scrollTop;
    lineCounter.scrollLeft = codeEditor.scrollLeft;
});

// Count the lines in the unencrypted testarea
var lineCountCache = 0;
function line_counter() {
      var lineCount = codeEditor.value.split('\n').length;
      var outarr = new Array();
      if (lineCountCache != lineCount) {
         for (var x = 0; x < lineCount; x++) {
            outarr[x] = (x + 1);
         }
         lineCounter.value = outarr.join('\n');
      }
      lineCountCache = lineCount;
}
codeEditor.addEventListener('input', () => {
    line_counter();
});

// Dynamically resize the line counter when the main textarea changes size
var resizer = function(sourceElement, targetElement, useOuterHeight) {
    var resizeInt = null;
    var resizeEvent = function() {
        if(useOuterHeight){
            targetElement.css("height", sourceElement.outerHeight(true));
        } else {
            targetElement.css("height", sourceElement.height());
        }

    };

    //Resize when textarea is resized
    sourceElement.on("mousedown", function(e) {
        resizeInt = setInterval(resizeEvent, 100 / 15);
    });
    $(window).on("mouseup", function(e) {
        if (resizeInt !== null) {
            clearInterval(resizeInt);
        }
        resizeEvent();
    });
}

// Run resizer for the line counter
lineCounterJQ.css("height", codeEditorJQ.outerHeight(true));
resizer(codeEditorJQ, lineCounterJQ, true);

// Download Encrypted textarea contents
function downloadFile(filename, content) {
    // It works on all HTML5 Ready browsers as it uses the download attribute of the <a> element:
    const element = document.createElement('a');

    //A blob is a data type that can store binary data
    // “type” is a MIME type
    // It can have a different value, based on a file you want to save
    const blob = new Blob([content], { type: 'plain/text' });
    //createObjectURL() static method creates a DOMString containing a URL representing the object given in the parameter.
    const fileUrl = URL.createObjectURL(blob);

    //setAttribute() Sets the value of an attribute on the specified element.
    element.setAttribute('href', fileUrl); //file location
    element.setAttribute('download', filename); // file name
    element.style.display = 'none';

    //use appendChild() method to move an element from one element to another
    document.body.appendChild(element);
    element.click();

    //The removeChild() method of the Node interface removes a child node from the DOM and returns the removed node
    document.body.removeChild(element);
};

// Add event listener for download button
window.onload = () => {
document.getElementById('download').
addEventListener('click', e => {
    const filename = document.getElementById('filename').value;
    const content = document.getElementById('encrypted').value;

    if (filename && content) {
    downloadFile(filename, content);
    }
});
};

// Set file name by mode
function setFilename(mode, file=""){
    if(mode == "raw"){
        document.getElementById('filename').value = "sealed-secret.txt"
    } else if(mode == "file"){
        document.getElementById('filename').value = file.name+"-sealed.txt"
    }
}