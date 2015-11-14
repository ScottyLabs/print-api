// drive upload
var CLIENT_ID = '839944436124-rem1av534i26hvb981oit811hkvphivr.apps.googleusercontent.com';

var SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
];

var pickerApiLoaded = false;
var oauthToken;

function driveBtnClick() {
    gapi.load('auth', {'callback': onAuthApiLoad});
    gapi.load('picker', {'callback': onPickerApiLoad});
}

function onAuthApiLoad() {
    window.gapi.auth.authorize(
    {
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'immediate': false
    },
    handleAuthResult);
}

function onPickerApiLoad() {
    pickerApiLoaded = true;
    createPicker();
}

function handleAuthResult(authResult) {
    if (authResult && !authResult.error) {
        oauthToken = authResult.access_token;
        createPicker();
    }
}

function createPicker() {
    if (pickerApiLoaded && oauthToken) {
        var picker = new google.picker.PickerBuilder().
        addView(google.picker.ViewId.DOCUMENTS).
        setOAuthToken(oauthToken).
        setCallback(pickerCallback).
        build();
        picker.setVisible(true);
    }
}

function pickerCallback(data) {
    if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
        var doc = data[google.picker.Response.DOCUMENTS][0];

        var fileURL = "https://www.googleapis.com/drive/v2/files/" + doc.id.toString();

        // first get file info and download link
        var xhr = new XMLHttpRequest();
        var accessToken = gapi.auth.getToken().access_token;
        xhr.open("GET", fileURL);
        xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
        xhr.responseType = "json";
        xhr.onload = function()
        {
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
            xhr2.onload = function()
            {
                var blob = xhr2.response;
                var f = new File([blob], res.title);
                console.log(f);
                postFile(f);
            }
            xhr2.send();
        }
        xhr.send();
    }
}


function postFile(file) {
    var formData = new FormData();
    formData.append("toPrint", file);
    var request = new XMLHttpRequest();
    request.open("POST", "http://localhost:8080/upload/hmuthaka");
    request.responseType = "json";
    request.send(formData);
}

// dropbox upload
options = {
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
            postFile(f);
        }
        xhr.send();
    },
    linkType: "direct",
    multiselect: false,
    extensions: ['.pdf', '.doc', '.docx'],
};

function dboxBtnClick() {
    Dropbox.choose(options);
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
