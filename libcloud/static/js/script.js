 $(function(){
	$(".dropdown-menu > li > a.trigger").on("click",function(e){
		var current=$(this).next();
		var grandparent=$(this).parent().parent();
		if($(this).hasClass('left-caret')||$(this).hasClass('right-caret'))
			$(this).toggleClass('right-caret left-caret');
		grandparent.find('.left-caret').not(this).toggleClass('right-caret left-caret');
		grandparent.find(".sub-menu:visible").not(current).hide();
		current.toggle();
		e.stopPropagation();
	});
	$(".dropdown-menu > li > a:not(.trigger)").on("click",function(){
		var root=$(this).closest('.dropdown');
		window.location = $(this).attr("href");
		root.find('.left-caret').toggleClass('right-caret left-caret');
		root.find('.sub-menu:visible').hide();
	});
});

var setCookie = function (n, val) {
    var exdays = 30;
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = n + "=" + val + "; " + expires;
};

var getCookie = function (n) {
    var name = n + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};

document.onclick = function (e) {
    if (e.target.className == 'btn') {
        var favColor = e.target.style.backgroundColor;
        setCookie('color', favColor);
        document.body.style.backgroundColor = favColor;
        console.log(favColor);
    }
};

window.onload = function () {
    var favColor = document.body.style.backgroundColor;
    var color = getCookie('color');
    if (color === '') {
        document.body.style.backgroundColor = favColor;

    } else {
      document.body.style.backgroundColor = color;
    }
    console.log("*");
    console.log(color);
};