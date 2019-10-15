export function textFromWords(words) {
    var text = '';

    words.forEach((word, i) => {
        let others = word['others'] ? word['others'] : {};
        let isPunct = ('type' in others) && (others['type'] == 'punctuation');

        if (i > 0 && !isPunct) {
            text += ' ';
        }

        text += word['word'];
    })

    return text;
};

export function getUrlParameter(sParam, defVal) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }

    return defVal;
};
