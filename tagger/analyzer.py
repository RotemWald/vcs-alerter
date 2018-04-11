from tagger import sentence_tagger

if __name__ == '__main__':
    example = "אז שני הקטעי אמצעים מקבילים לאלכסון ואז נוכל להוכיח שיש זוג צלעות נגדיות מקבילות.... ואם נשרטט אלכסון שני נוכל להוכיח גם כן את אותו דבר ולמצוא עוד זוג צלעות"
    # example = "תשחרר את השליטה"
    # example = "מה דעתך על זה?"
    # example = 'נראלי שזה מעוין כי האלכסונים שוים זה לזה ומאונכים זה לזה'
    # example = "התשובה היא מרובע"

    sentence_tagger = sentence_tagger.SentenceTagger()

    print(sentence_tagger.tag_sentence(example))
