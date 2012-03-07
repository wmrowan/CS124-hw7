var fs = require('fs'),
    http = require('http'),
    util = require('util'),
    _ = require('underscore');

var mots = _.filter(fs.readFileSync("french.txt", "utf8").split(/\s+/), function(w){ return w != '' && w != null });

var dictionaryApiBase = "";

var translations = {},
    numToTranslate = mots.length;

_(mots).each(function(mot) {
  mot = mot.replace(/\W*$/, '');

  var getData = {
    host: 'api.wordreference.com',
    port: 80,
    path: escape('/' + ['0.8', '3d232', 'json', 'fren', mot].join('/')),
    headers: {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21' 
    }
  };

  http.get(getData, function(res) {
    var datArr = [];
    res.on('data', function(d){ datArr.push(d.toString('utf8')); });
    res.on('end', function() {
      //console.log(datArr)
      var data = JSON.parse(datArr.join(''));

      if(data.Error) {
        console.log("THERE WAS AN ERROR FOR WORD: " + mot);
        console.log(data.Error);
        process.exit(1);
      }

      var level1 = data.term0 || data.Compounds || data.original || null,
          //level2 = level1.AdditionalTranslations || level1.PrincipalTranslations || level1.Compounds;
          level2 = level1.PrincipalTranslations || level1.AdditionalTranslations || level1.Compounds;

      var translation = level2[0].FirstTranslation.term;

      console.log("translation: " + mot + " -> " + translation);

      translations[mot] = translation;

      if(--numToTranslate == 0) {
        fs.writeFileSync("dictionary.json", JSON.stringify(translations));
      }

    })

  }).on('error', function(e){ throw e })

});

