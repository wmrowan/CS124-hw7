var fs = require('fs'),
    _ = require('underscore');

var frenchWords = fs.readFileSync("french.txt", "utf8").split(/\s+/),
    dictionary = JSON.parse(fs.readFileSync("dictionary.json")),
    englishWords = [];

_(frenchWords).each(function(frenchWord) {
  if(frenchWord == '') return;

  englishWords.push(dictionary[frenchWord]);
})

fs.writeFileSync("english.txt", englishWords.join(' ') + "\n");
