$(document).ready(function(){

    if($('#acquireFunction').attr('checked')) {
        $('#archetypes-fieldname-function').hide();
    }

    $('#acquireFunction').live("click", function() {
        if (this.checked) {
            $('#archetypes-fieldname-function').hide();
        }
        else {
            $('#archetypes-fieldname-function').show();
        }
    });
});