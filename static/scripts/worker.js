importScripts('string_score.min.js');

var data;
var DEBUG = false;


onmessage = function(e) {
    console.log(e)
    if (e.data.type === 'data') {
        if (DEBUG) console.log('Got data');
        data = e.data.data;
        for (var i = 0; i < data.length; ++i) {
            data[i] = {text: data[i].toLowerCase(), index: i, score: 0};
        }
    } else if (e.data.type === 'query') {
        var query = e.data.query;
        query = query.toLowerCase();
        var terms = query.split(/\s+/);
        var fuzz = 0.3;
        if (DEBUG) console.log('got query: ', query);
        for (var j = 0; j < data.length; ++j) {
            for (var t = 0; t < terms.length; ++t) {
                var maxTermScore = 0;
                var termFieldScore = data[j].text.score(terms[t], fuzz);
                if (termFieldScore > maxTermScore) {
                    maxTermScore = termFieldScore;
                }
                data[j].score += maxTermScore;
            }
        }
        data.sort(function(a, b) {
            return b.score - a.score;
        });
        if(query.length > 0)
            var results = data.slice(0, 4);
        else
            var results = data.slice(0, 0);
        if (DEBUG) console.log('results: ', results);
        postMessage(results);
        
        for (elem of data) {
            elem.score = 0;
        }
    }
};

