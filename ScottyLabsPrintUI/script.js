$(document).ready(function () {
    $('#uploadpage').hide();
    $('#aboutpage').hide();
    $('#helppage').hide();
    $('#uploadbutton').click(function () {
        $('#homepage').hide();
        $('#uploadpage').show(1000);
    });
    $('#sendbutton').click(function () {
        var fileName = $("#file").val();
        if (!$('#andrewID').val() && !fileName) {
            alert("Please fill out the form and try again.")
        } else if (!$('#andrewID').val()) {
            alert("Please input your Andrew ID and try again.");
        } else if (!fileName) {
            alert("Please select a file to upload and try again.");
        } else {
            alert("Successfully sent to the print queue!");
            location.reload();
        }
    });
    $('#aboutlink').click(function () {
        $('#homepage').hide();
        $('#uploadpage').hide();
        $('#helppage').hide();
        $('#aboutpage').show(1000);
    });
    $('#helplink').click(function () {
        $('#homepage').hide();
        $('#uploadpage').hide();
        $('#aboutpage').hide();
        $('#helppage').show(1000);
    });
    $('#back').click(function () {
        $('#aboutpage').hide();
        $('#uploadpage').hide();
        $('#helppage').hide();
        $('#homepage').show(1000);
    });
});