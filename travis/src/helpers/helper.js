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