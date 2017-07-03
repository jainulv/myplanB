var request = require('request');
var cheerio = require('cheerio');

var credentials = {
	weblogin_netid: 'jnv3',
	weblogin_password: '*@Ja#9824147318!'
};

request.post({
  	uri: 'http://weblogin.washington.edu/',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
	body: require('querystring').stringify(credentials)
}, function(err, res, body){
	if(err) {
	        callback.call(null, new Error('Login failed'));
		return;
	}

	request('http://www.washington.edu/cec/toc.html', function(err, res, body) {
		if(err) {
			callback.call(null, new Error('Request failed'));
			return;
		}

		var $ = cheerio.load(body);
	    var text = $('#element').text();
	    console.log(body)
	    console.log($)
	        console.log(text)
	});
});
