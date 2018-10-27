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
        .on('keydown.autocomplete', '.first-language', function() {
            $(this).autocomplete(autocomplete_options);
        })
        .on('keydown.autocomplete', '.other-language', function() {
            $(this).autocomplete(autocomplete_options);
        });

    $("#first-language-group")
        .on('click', '.add-first-language', function(e) {
            $('.add-first-language')
                .html("<i class=\"fas fa-minus\"></i>")
                .removeClass("btn-primary add-first-language")
                .addClass("btn-secondary remove-first-language");
            $("#first-language-group").append($("<div class=\"input-group\">\n" +
                "                        <input type=\"text\" class=\"form-control first-language\" placeholder=\"e.g. English\">\n" +
                "                        <div class=\"input-group-append\">\n" +
                "                            <button class=\"btn btn-primary add-first-language\" type=\"button\">\n" +
                "                                <i class=\"fas fa-plus\"></i>\n" +
                "                            </button>\n" +
                "                        </div>\n" +
                "                        <div class=\"dropdown input-group-append\">\n" +
                "                            <a class=\"btn btn-secondary dropdown-toggle\" data-display=\"static\" href=\"#\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
                "                                Fluency\n" +
                "                            </a>\n" +
                "                            <div class=\"dropdown-menu\">\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"1\">1 - Little experience, can use and understand basic sentences and questions</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"2\">2 - Some experience, can hold basic, casual conversations</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"3\">3 - Lots of experience, not quite fluent but can communicate well in the language</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"4\">4 - Fluent, no communication problems</a>\n" +
                "                            </div>\n" +
                "                        </div>\n" +
                "                    </div>"));
            e.preventDefault();
        })
        .on('click', '.remove-first-language', function(e) {
            $(this).closest('.input-group').remove();
            e.preventDefault();
        })
        .on('click', '.dropdown-menu a', function(e) {
            // TODO: mobile styling, more responsive
            let optionText = $(this).text().substr(0, 20) + "...";
            $(this).parents('.dropdown').find('.dropdown-toggle')
                .html(optionText);
            e.preventDefault();
        });


    $("#other-language-group")
        .on('click', '.add-other-language', function(e) {
            $('.add-other-language')
                .html("<i class=\"fas fa-minus\"></i>")
                .removeClass("btn-primary add-other-language")
                .addClass("btn-secondary remove-other-language");
            $("#other-language-group").append($("<div class=\"input-group\">\n" +
                "                        <input type=\"text\" class=\"form-control other-language\" placeholder=\"e.g. Woods Cree\">\n" +
                "                        <div class=\"input-group-append\">\n" +
                "                            <button class=\"btn btn-primary add-other-language\" type=\"button\">\n" +
                "                                <i class=\"fas fa-plus\"></i>\n" +
                "                            </button>\n" +
                "                        </div>\n" +
                "                        <div class=\"dropdown input-group-append\">\n" +
                "                            <a class=\"btn btn-secondary dropdown-toggle\" data-display=\"static\" href=\"#\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
                "                                Fluency\n" +
                "                            </a>\n" +
                "                            <div class=\"dropdown-menu\">\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"1\">1 - Little experience, can use and understand basic sentences and questions</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"2\">2 - Some experience, can hold basic, casual conversations</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"3\">3 - Lots of experience, not quite fluent but can communicate well in the language</a>\n" +
                "                                <a class=\"dropdown-item\" href=\"\" value=\"4\">4 - Fluent, no communication problems</a>\n" +
                "                            </div>\n" +
                "                        </div>\n" +
                "                    </div>"));
            e.preventDefault();
        })
        .on('click', '.remove-other-language', function(e) {
            $(this).closest('.input-group').remove();
            e.preventDefault();
        })
        .on('click', '.dropdown-menu a', function(e) {
            // TODO: mobile styling, more responsive
            let optionText = $(this).text().substr(0, 20) + "...";
            $(this).parents('.dropdown').find('.dropdown-toggle')
                .html(optionText);
            e.preventDefault();
        });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // TODO: Delaney help... right now I'm not doing anything with the data
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