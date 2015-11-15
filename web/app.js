/* @file app.js 
 * @brief Contains the auth libraries for Google Drive, Dropzone, and Dropbox.
 */

var printSL = {};
console.log("Initialized print.");

printSL.gdrive = {};

printSL.gdrive.config = {};
printSL.gdrive.config.CLIENT_ID = '839944436124-rem1av534i26hvb981oit811hkvphivr.apps.googleusercontent.com';
printSL.gdrive.config.SCOPES = ['https://www.googleapis.com/auth/drive.file'];


printSL.gdrive.pickerApiLoaded = false;
printSL.gdrive.oauthToken;

printSL.gdrive.onclick = function () {
  gapi.load('auth', {'callback': printSL.gdrive.onAuthApiLoad});
  gapi.load('picker', {'callback': printSL.gdrive.onPickerApiLoad});
};

printSL.gdrive.onAuthApiLoad = function() {
  window.gapi.auth.authorize(
    {
      'client_id': printSL.gdrive.config.CLIENT_ID,
      'scope': printSL.gdrive.config.SCOPES,
      'immediate': false
    },
    printSL.gdrive.handleAuthResult);
};

printSL.gdrive.onPickerApiLoad = function() {
  pickerApiLoaded = true;
  printSL.gdrive.createPicker();
};

printSL.gdrive.handleAuthResult = function(authResult) {
  if (authResult && !authResult.error) {
    printSL.gdrive.oauthToken = authResult.access_token;
    printSL.gdrive.createPicker();
  }
};

printSL.gdrive.createPicker = function() {
  if (printSL.gdrive.pickerApiLoaded && printSL.gdrive.oauthToken) {
    var picker = new google.picker.PickerBuilder()
      .addView(google.picker.ViewId.DOCUMENTS)
      .setOAuthToken(oauthToken)
      .setCallback(pickerCallback)
      .build();
    picker.setVisible(true);
  }
};

printSL.gdrive.pickerCallback = function(data) {
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    var doc = data[google.picker.Response.DOCUMENTS][0];

    var fileURL = "https://www.googleapis.com/drive/v2/files/" + doc.id.toString();

    // first get file info and download link
    var xhr = new XMLHttpRequest();
    var accessToken = gapi.auth.getToken().access_token;
    xhr.open("GET", fileURL);
    xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
    xhr.responseType = "json";
    xhr.onload = function() {
      var res = xhr.response;
      var url;
      if (res.downloadUrl)
        url = res.downloadUrl;
      else
        url = res.exportLinks['application/pdf'];

      // get file
      var xhr2 = new XMLHttpRequest();
      xhr2.open("GET", url);
      xhr2.setRequestHeader('Authorization', 'Bearer ' + accessToken);
      xhr2.responseType = "blob";
      xhr2.onload = function() {
        var blob = xhr2.response;
        var f = new File([blob], res.title);
        console.log(f);
        printSL.postFile(f);
      }
      xhr2.send();
    }
    xhr.send();
  }
}


printSL.postFile = function(file) {
  var formData = new FormData();
  formData.append("toPrint", file);
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:8080/upload/hmuthaka");
  request.responseType = "json";
  request.send(formData);
}

printSL.dropbox = {};

// dropbox upload
printSL.dropbox.config = {
  success: function(files) {
    var url = files[0].link;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.responseType = "blob";
    xhr.onload = function()
    {
      var blob = xhr.response;
      var f = new File([blob], files[0].name);
      console.log(f);
      printSL.postFile(f);
    }
    xhr.send();
  },
  linkType: "direct",
  multiselect: false,
  extensions: ['.pdf', '.doc', '.docx'],
};

printSL.dropbox.onclick = function() {
  Dropbox.choose(printSL.dropbox.config);
}

// direct/drag-and-drop file upload
Dropzone.options.printDropzone = {
  paramName: "toPrint",
  init: function()  {
    this.on("addedfile", function(file) {
      console.log(file);
    });
  }
};
