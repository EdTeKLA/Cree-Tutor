// TODO: make fluencyLevels more dynamic
// TODO: refactor dropdown menu... get rid of value on a element
const setLanguageGroup = function(id, placeholder, fluencyLevels) {
    let inputGroupString =
        "<div class=\"input-group\">\n" +
        "    <input type=\"text\" class=\"form-control " + id + "\" placeholder=\"" + placeholder + "\">\n";

    if (fluencyLevels && fluencyLevels.length > 0) {
        inputGroupString +=
            "<div class=\"dropdown-wrap input-group-append\" data-content=\"\">\n" +
            "    <select class=\"dropdown\">\n" +
            "        <option value=\"" + fluencyLevels[0] +"\">\n" +
            "        " + fluencyLevels[0] +
            "        </option>\n" +
            "        <option value=\"" + fluencyLevels[1] +"\">\n" +
            "        " + fluencyLevels[1] +
            "        </option>\n" +
            "        <option value=\"" + fluencyLevels[2] +"\">\n" +
            "        " + fluencyLevels[2] +
            "        </option>\n" +
            "        <option value=\"" + fluencyLevels[3] +"\">\n" +
            "        " + fluencyLevels[3] +
            "        </option>\n" +
            "    </select>\n" +
            "</div>"
    }

    inputGroupString +=
        "    <div class=\"input-group-append\">\n" +
        "        <button class=\"btn btn-primary remove-" + id + "\" type=\"button\">\n" +
        "            <i class=\"fas fa-minus\"></i>" +
        "        </button>\n" +
        "    </div>" +
        "</div>";

    setSelect($("#" + id + "-group div.input-group"));

    $("#" + id + "-group")
        .on('click', '.add-' + id, function(e) {
            let toAppend = $(inputGroupString);
            setSelect(toAppend);
            $("#" + id + "-input-group").append(toAppend);
            e.preventDefault();
        })
        .on('click', '.remove-' + id, function(e) {
            $(this).closest('.input-group').remove();
            e.preventDefault();
        });
};

const setHelpText = function(id) {
    $('#' + id + '-help').on('click', function(e) {
        const helpText = $('#' + id + '-help-text');

        if (helpText.hasClass('closed')) {
            helpText.removeClass('closed');
        } else {
            helpText.addClass('closed');
        }
        e.preventDefault();
    });
};

const handleSelectChange = function(e, container) {
    container.attr('data-content', e.currentTarget.value);
};

const setSelect = function(parent) {
    let selectContainer = parent.find("div.dropdown-wrap");
    let select = selectContainer.find("select.dropdown");

    select.value = "Fluency";
    selectContainer.attr('data-content', select.value);
    select.on('change', (e) => {
        handleSelectChange(e, selectContainer);
    });
};

$(function () {
    $("[data-toggle=tooltip]").tooltip({
        boundary: 'viewport',
        placement: 'right',
        container: 'body',
    });

    $(".custom-tooltip").on("click", function(e) {
        e.preventDefault();
    });

    const autocomplete_options = {
        source: languages
    };
    $(document)
        .on('keydown.autocomplete', '.primary-language, .additional-primary-language, .other-language', function() {
            $(this).autocomplete(autocomplete_options);
        });

    // Set the language fluency dropdown
    setLanguageGroup('additional-primary-language', 'e.g. French');

    setLanguageGroup('other-language', 'e.g. Wood Cree', [
        '1 - Little experience, can use and understand basic sentences and questions',
        '2 - Some experience, can hold basic, casual conversations',
        '3 - Lots of experience, not quite fluent but can communicate well in the language',
        '4 - Fluent, no communication problems'
    ]);

    // Set the help text click event
    setHelpText('primary-language');
    setHelpText('additional-primary-language');
    setHelpText('other-language');

    // If the user answers yes to knowing more languages, show two additional questions.
    $('input[name=more-languages]').on('change', function() {
        if (this.value === 'yes') {
            $('#additional-primary-language-group').removeClass('hidden');
            $('#other-language-group').removeClass('hidden');
        }
        if (this.value === 'no') {
            $('#additional-primary-language-group').addClass('hidden');
            $('#other-language-group').addClass('hidden');
        }
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