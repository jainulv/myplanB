$(document).ready(function() {
    var max_fields      = 5; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
    var submit          = $(".submit");           //Submit button ID
    
    var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(add_button).detach(); //detach the add button
            $(submit).detach(); // detach the submit button
            $(wrapper).append('<div>Course name: <input type="text" name="coursename"/> Rating: <input type="text" name="coursename"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
            $(wrapper).append(add_button); // add back the add button
            $(wrapper).append(submit); // add back the submit button
        }
        if (x > max_fields - 1) {
            $(add_button).detach()  // remove add button once the user has exhausted max_fields
        }
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault();
        if (x > max_fields - 1) { // if add button is absent, put it back
            $(submit).detach();
            $(wrapper).append(add_button);
            $(wrapper).append(submit);
        }
        $(this).parent('div').remove(); 
        x--;
    })
});
