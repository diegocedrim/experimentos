
$(document).ready(function(){
    var parseleyValidator = $('#form_smells_relevance').parsley({
//        successClass: "has-success",
        errorClass: "has-error",
        classHandler: function(el) {
            return el.$element.closest(".form-group");
        },
        errorsWrapper: "<span class='help-block'></span>",
        errorTemplate: "<span></span>"
    });

    parseleyValidator.on('field:success', function(el) {
        el.$element.closest("dl").removeClass("text-danger");
    });

    parseleyValidator.on('field:error', function(el) {
        el.$element.closest("dl").addClass("text-danger");
    });

//    $("input[type=radio]").on("click", function() {
//        parseleyValidator.validate();
//    });
});