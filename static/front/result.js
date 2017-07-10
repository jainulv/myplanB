$(document).ready(function(){
    var headers = document.getElementsByTagName('header');
    var a_lowers = document.getElementsByTagName('div');
    var colors = ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#FFC107'];
    var light_colors =['#FFCDD2', '#F8BBD0', '#E1BEE7', '#D1C4E9', '#C5CAE9', '#BBDEFB', '#B3E5FC', '#B2EBF2', '#B2DFDB', '#C8E6C9', '#FFECB3'];
    var lowers = []
    for (var i = 0; i < a_lowers.length; i++) {
        if ($(a_lowers[i]).attr('class') == 'w3-container') {
            lowers.push(a_lowers[i]);
        }
    }
    for (var i = 0; i < headers.length; i++) {
        var random_color = Math.floor(Math.random() * colors.length);
        headers[i].style.background=colors[random_color];
        lowers[i].style.background=light_colors[random_color];
    }
});

