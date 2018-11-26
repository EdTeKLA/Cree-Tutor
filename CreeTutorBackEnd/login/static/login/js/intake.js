// TODO: make fluencyLevels more dynamic
// TODO: refactor dropdown menu... get rid of value on a element
const setLanguageGroup = function(id, placeholder, fluencyLevels) {
    let inputGroupString =
        "<div class=\"input-group\">\n" +
        "    <input type=\"text\" class=\"form-control " + id + "\" placeholder=\"" + placeholder + "\">\n";

    if (fluencyLevels && fluencyLevels.length > 0) {
        inputGroupString +=
            "<div class=\"dropdown input-group-append\">\n" +
            "    <a class=\"btn btn-secondary dropdown-toggle\" data-display=\"static\" href=\"#\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
            "        <span>Fluency</span>\n" +
            "    </a>\n" +
            "    <div class=\"dropdown-menu dropdown-menu-right\">\n" +
            "        <a class=\"dropdown-item\" href=\"\" value=\"1\">" + fluencyLevels[0] + "</a>\n" +
            "        <a class=\"dropdown-item\" href=\"\" value=\"2\">" + fluencyLevels[1] + "</a>\n" +
            "        <a class=\"dropdown-item\" href=\"\" value=\"3\">" + fluencyLevels[2] + "</a>\n" +
            "        <a class=\"dropdown-item\" href=\"\" value=\"4\">" + fluencyLevels[3] + "</a>\n" +
            "    </div>\n" +
            "</div>\n";
    }

    inputGroupString +=
        "    <div class=\"input-group-append\">\n" +
        "        <button class=\"btn btn-primary remove-" + id + "\" type=\"button\">\n" +
        "            <i class=\"fas fa-minus\"></i>" +
        "        </button>\n" +
        "    </div>" +
        "</div>";

    $("#" + id + "-group")
        .on('click', '.add-' + id, function(e) {
            $("#" + id + "-input-group").append($(inputGroupString));
            e.preventDefault();
        })
        .on('click', '.remove-' + id, function(e) {
            $(this).closest('.input-group').remove();
            e.preventDefault();
        })
        .on('click', '.dropdown-menu a', function(e) {
            let optionText = $(this).text();
            $(this).parents('.dropdown').find('.dropdown-toggle span')
                .html(optionText);
            e.preventDefault();
        });
};

$(function () {
    $("[data-toggle=tooltip]").tooltip({
        boundary: 'viewport',
        placement: 'right',
        container: 'body',
    });

    const autocomplete_options = {
        source: languages
    };
    $(document)
        .on('keydown.autocomplete', '.first-language, .other-language', function() {
            $(this).autocomplete(autocomplete_options);
        });

    setLanguageGroup('first-language', 'e.g. English', [
        'Spoke only as a child, no longer understand or speak the language',
        'Can still understand, but cannot speak very well',
        'Can still understand and speak, but not fluently',
        'Can speak fluently'
    ]);

    setLanguageGroup('other-language', 'e.g. Wood Cree', [
        'Little experience, can use and understand basic sentences and questions',
        'Some experience, can hold basic, casual conversations',
        'Lots of experience, not quite fluent but can communicate well in the language',
        'Fluent, no communication problems'
    ]);

    $('#first-language-help').on('click', function(e) {
        const firstLanguageHelpText = $('#first-language-help-text');

        if (firstLanguageHelpText.hasClass('closed')) {
            firstLanguageHelpText.removeClass('closed');
        } else {
            firstLanguageHelpText.addClass('closed');
        }
        e.preventDefault();
    });
    $('#other-language-help').on('click', function(e) {
        const otherLanguageHelpText = $('#other-language-help-text');

        if (otherLanguageHelpText.hasClass('closed')) {
            otherLanguageHelpText.removeClass('closed');
        } else {
            otherLanguageHelpText.addClass('closed');
        }
        e.preventDefault();
    });

    // TODO: do something with the data?
    $(document).on('submit', '#intake-form', function(e){
        e.preventDefault();

        $.ajax({
            type:'POST',
            url: "/submit_intake/",
            success: function(data) {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});

// right now copied from languages.json because i didn't want to load in the file
languages = [
    "Afar",
    "Abkhazian",
    "Avestan",
    "Afrikaans",
    "Akan",
    "Amharic",
    "Aragonese",
    "Arabic",
    "Assamese",
    "Avaric",
    "Aymara",
    "Azerbaijani",
    "Bashkir",
    "Belarusian",
    "Bulgarian",
    "Bihari languages",
    "Bislama",
    "Bambara",
    "Bengali",
    "Tibetan",
    "Breton",
    "Bosnian",
    "Catalan; Valencian",
    "Chechen",
    "Chamorro",
    "Corsican",
    "Cree",
    "Czech",
    "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic",
    "Chuvash",
    "Welsh",
    "Danish",
    "German",
    "Divehi; Dhivehi; Maldivian",
    "Dzongkha",
    "Ewe",
    "Greek Modern (1453)",
    "English",
    "Esperanto",
    "Spanish; Castilian",
    "Estonian",
    "Basque",
    "Persian",
    "Fulah",
    "Finnish",
    "Fijian",
    "Faroese",
    "French",
    "Western Frisian",
    "Irish",
    "Gaelic; Scottish Gaelic",
    "Galician",
    "Guarani",
    "Gujarati",
    "Manx",
    "Hausa",
    "Hebrew",
    "Hindi",
    "Hiri Motu",
    "Croatian",
    "Haitian; Haitian Creole",
    "Hungarian",
    "Armenian",
    "Herero",
    "Interlingua (International Auxiliary Language Association)",
    "Indonesian",
    "Interlingue; Occidental",
    "Igbo",
    "Sichuan Yi; Nuosu",
    "Inupiaq",
    "Ido",
    "Icelandic",
    "Italian",
    "Inuktitut",
    "Japanese",
    "Javanese",
    "Georgian",
    "Kongo",
    "Kikuyu; Gikuyu",
    "Kuanyama; Kwanyama",
    "Kazakh",
    "Kalaallisut; Greenlandic",
    "Central Khmer",
    "Kannada",
    "Korean",
    "Kanuri",
    "Kashmiri",
    "Kurdish",
    "Komi",
    "Cornish",
    "Kirghiz; Kyrgyz",
    "Latin",
    "Luxembourgish; Letzeburgesch",
    "Ganda",
    "Limburgan; Limburger; Limburgish",
    "Lingala",
    "Lao",
    "Lithuanian",
    "LubaKatanga",
    "Latvian",
    "Malagasy",
    "Marshallese",
    "Maori",
    "Macedonian",
    "Malayalam",
    "Mongolian",
    "Marathi",
    "Malay",
    "Maltese",
    "Burmese",
    "Nauru",
    "Bokml Norwegian; Norwegian Bokml",
    "Ndebele North; North Ndebele",
    "Nepali",
    "Ndonga",
    "Dutch; Flemish",
    "Norwegian Nynorsk; Nynorsk Norwegian",
    "Norwegian",
    "Ndebele South; South Ndebele",
    "Navajo; Navaho",
    "Chichewa; Chewa; Nyanja",
    "Occitan (post 1500); Provenal",
    "Ojibwa",
    "Oromo",
    "Oriya",
    "Ossetian; Ossetic",
    "Panjabi; Punjabi",
    "Pali",
    "Polish",
    "Pushto; Pashto",
    "Portuguese",
    "Quechua",
    "Romansh",
    "Rundi",
    "Romanian; Moldavian; Moldovan",
    "Russian",
    "Kinyarwanda",
    "Sanskrit",
    "Sardinian",
    "Sindhi",
    "Northern Sami",
    "Sango",
    "Sinhala; Sinhalese",
    "Slovak",
    "Slovenian",
    "Samoan",
    "Shona",
    "Somali",
    "Albanian",
    "Serbian",
    "Swati",
    "Sotho Southern",
    "Sundanese",
    "Swedish",
    "Swahili",
    "Tamil",
    "Telugu",
    "Tajik",
    "Thai",
    "Tigrinya",
    "Turkmen",
    "Tagalog",
    "Tswana",
    "Tonga (Tonga Islands)",
    "Turkish",
    "Tsonga",
    "Tatar",
    "Twi",
    "Tahitian",
    "Uighur; Uyghur",
    "Ukrainian",
    "Urdu",
    "Uzbek",
    "Venda",
    "Vietnamese",
    "Volapk",
    "Walloon",
    "Wolof",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Zhuang; Chuang",
    "Chinese",
    "Zulu"
];