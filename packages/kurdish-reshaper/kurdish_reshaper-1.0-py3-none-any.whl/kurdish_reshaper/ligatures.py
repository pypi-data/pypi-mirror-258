# Each ligature is of the format:
#
#   ('<key>', <replacement>)
#
# Where <key> is used in the configuration and <replacement> is of the format:
#
#   ('<match>', ('<isolated>', '<initial>', '<medial>', '<final>'))
#
# Where <match> is the string to replace, and <isolated> is the replacement in
# case <match> was in isolated form, <initial> is the replacement in case
# <match> was in initial form, <medial> is the replacement in case <match> was
# in medial form, and <final> is the replacement in case <match> was in final
# form. If no replacement is specified for a form, then no replacement of
# <match> will occur.

# Order here is important, it should be:
#   1. Sentences
#   2. Words
#   3. Letters
# This way we make sure we replace the longest ligatures first

from itertools import chain

SENTENCES_LIGATURES = (
    ('Kurdish LIGATURE BISMILLAH AR-RAHMAN AR-RAHEEM', (
        '\u0628\u0633\u0645\u0020'
        '\u0627\u0644\u0644\u0647\u0020'
        '\u0627\u0644\u0631\u062D\u0645\u0646\u0020'
        '\u0627\u0644\u0631\u062D\u064A\u0645',

        ('\uFDFD', '', '', '')
    )),
    ('Kurdish LIGATURE JALLAJALALOUHOU', (
        '\u062C\u0644\u0020\u062C\u0644\u0627\u0644\u0647',

        ('\uFDFB', '', '', '')
    )),
    ('Kurdish LIGATURE SALLALLAHOU ALAYHE WASALLAM', (
        '\u0635\u0644\u0649\u0020'
        '\u0627\u0644\u0644\u0647\u0020'
        '\u0639\u0644\u064A\u0647\u0020'
        '\u0648\u0633\u0644\u0645',

        ('\uFDFA', '', '', '')
    )),
)

WORDS_LIGATURES = (
    ('Kurdish LIGATURE ALLAH', (
        '\u0627\u0644\u0644\u0647', ('\uFDF2', '', '', ''),
    )),
    ('Kurdish LIGATURE AKBAR', (
        '\u0623\u0643\u0628\u0631', ('\uFDF3', '', '', ''),
    )),
    ('Kurdish LIGATURE ALAYHE', (
        '\u0639\u0644\u064A\u0647', ('\uFDF7', '', '', ''),
    )),
    ('Kurdish LIGATURE MOHAMMAD', (
        '\u0645\u062D\u0645\u062F', ('\uFDF4', '', '', ''),
    )),
    ('Kurdish LIGATURE RASOUL', (
        '\u0631\u0633\u0648\u0644', ('\uFDF6', '', '', ''),
    )),
    ('Kurdish LIGATURE SALAM', (
        '\u0635\u0644\u0639\u0645', ('\uFDF5', '', '', ''),
    )),
    ('Kurdish LIGATURE SALLA', (
        '\u0635\u0644\u0649', ('\uFDF9', '', '', ''),
    )),
    ('Kurdish LIGATURE WASALLAM', (
        '\u0648\u0633\u0644\u0645', ('\uFDF8', '', '', ''),
    )),
    ('RIAL SIGN', (
        '\u0631[\u06CC\u064A]\u0627\u0644', ('\uFDFC', '', '', ''),
    )),
)

LETTERS_LIGATURES = (
    ('Kurdish LIGATURE AIN WITH ALEF MAKSURA', (
        '\u0639\u0649', ('\uFCF7', '', '', '\uFD13'),
    )),
    ('Kurdish LIGATURE AIN WITH JEEM', (
        '\u0639\u062C', ('\uFC29', '\uFCBA', '', ''),
    )),
    ('Kurdish LIGATURE AIN WITH JEEM WITH MEEM', (
        '\u0639\u062C\u0645', ('', '\uFDC4', '', '\uFD75'),
    )),
    ('Kurdish LIGATURE AIN WITH MEEM', (
        '\u0639\u0645', ('\uFC2A', '\uFCBB', '', ''),
    )),
    ('Kurdish LIGATURE AIN WITH MEEM WITH ALEF MAKSURA', (
        '\u0639\u0645\u0649', ('', '', '', '\uFD78'),
    )),
    ('Kurdish LIGATURE AIN WITH MEEM WITH MEEM', (
        '\u0639\u0645\u0645', ('', '\uFD77', '', '\uFD76'),
    )),
    ('Kurdish LIGATURE AIN WITH MEEM WITH YEH', (
        '\u0639\u0645\u064A', ('', '', '', '\uFDB6'),
    )),
    ('Kurdish LIGATURE AIN WITH YEH', (
        '\u0639\u064A', ('\uFCF8', '', '', '\uFD14'),
    )),
    ('Kurdish LIGATURE ALEF MAKSURA WITH SUPERSCRIPT ALEF', (
        '\u0649\u0670', ('\uFC5D', '', '', '\uFC90'),
    )),
    ('Kurdish LIGATURE ALEF WITH FATHATAN', (
        '\u0627\u064B', ('\uFD3D', '', '', '\uFD3C'),
    )),
    ('Kurdish LIGATURE BEH WITH ALEF MAKSURA', (
        '\u0628\u0649', ('\uFC09', '', '', '\uFC6E'),
    )),
    ('Kurdish LIGATURE BEH WITH HAH', (
        '\u0628\u062D', ('\uFC06', '\uFC9D', '', ''),
    )),
    ('Kurdish LIGATURE BEH WITH HAH WITH YEH', (
        '\u0628\u062D\u064A', ('', '', '', '\uFDC2'),
    )),
    ('Kurdish LIGATURE BEH WITH HEH', (
        '\u0628\u0647', ('', '\uFCA0', '\uFCE2', ''),
    )),
    ('Kurdish LIGATURE BEH WITH JEEM', (
        '\u0628\u062C', ('\uFC05', '\uFC9C', '', ''),
    )),
    ('Kurdish LIGATURE BEH WITH KHAH', (
        '\u0628\u062E', ('\uFC07', '\uFC9E', '', ''),
    )),
    ('Kurdish LIGATURE BEH WITH KHAH WITH YEH', (
        '\u0628\u062E\u064A', ('', '', '', '\uFD9E'),
    )),
    ('Kurdish LIGATURE BEH WITH MEEM', (
        '\u0628\u0645', ('\uFC08', '\uFC9F', '\uFCE1', '\uFC6C'),
    )),
    ('Kurdish LIGATURE BEH WITH NOON', (
        '\u0628\u0646', ('', '', '', '\uFC6D'),
    )),
    ('Kurdish LIGATURE BEH WITH REH', (
        '\u0628\u0631', ('', '', '', '\uFC6A'),
    )),
    ('Kurdish LIGATURE BEH WITH YEH', (
        '\u0628\u064A', ('\uFC0A', '', '', '\uFC6F'),
    )),
    ('Kurdish LIGATURE BEH WITH ZAIN', (
        '\u0628\u0632', ('', '', '', '\uFC6B'),
    )),
    ('Kurdish LIGATURE DAD WITH ALEF MAKSURA', (
        '\u0636\u0649', ('\uFD07', '', '', '\uFD23'),
    )),
    ('Kurdish LIGATURE DAD WITH HAH', (
        '\u0636\u062D', ('\uFC23', '\uFCB5', '', ''),
    )),
    ('Kurdish LIGATURE DAD WITH HAH WITH ALEF MAKSURA', (
        '\u0636\u062D\u0649', ('', '', '', '\uFD6E'),
    )),
    ('Kurdish LIGATURE DAD WITH HAH WITH YEH', (
        '\u0636\u062D\u064A', ('', '', '', '\uFDAB'),
    )),
    ('Kurdish LIGATURE DAD WITH JEEM', (
        '\u0636\u062C', ('\uFC22', '\uFCB4', '', ''),
    )),
    ('Kurdish LIGATURE DAD WITH KHAH', (
        '\u0636\u062E', ('\uFC24', '\uFCB6', '', ''),
    )),
    ('Kurdish LIGATURE DAD WITH KHAH WITH MEEM', (
        '\u0636\u062E\u0645', ('', '\uFD70', '', '\uFD6F'),
    )),
    ('Kurdish LIGATURE DAD WITH MEEM', (
        '\u0636\u0645', ('\uFC25', '\uFCB7', '', ''),
    )),
    ('Kurdish LIGATURE DAD WITH REH', (
        '\u0636\u0631', ('\uFD10', '', '', '\uFD2C'),
    )),
    ('Kurdish LIGATURE DAD WITH YEH', (
        '\u0636\u064A', ('\uFD08', '', '', '\uFD24'),
    )),
    ('Kurdish LIGATURE FEH WITH ALEF MAKSURA', (
        '\u0641\u0649', ('\uFC31', '', '', '\uFC7C'),
    )),
    ('Kurdish LIGATURE FEH WITH HAH', (
        '\u0641\u062D', ('\uFC2E', '\uFCBF', '', ''),
    )),
    ('Kurdish LIGATURE FEH WITH JEEM', (
        '\u0641\u062C', ('\uFC2D', '\uFCBE', '', ''),
    )),
    ('Kurdish LIGATURE FEH WITH KHAH', (
        '\u0641\u062E', ('\uFC2F', '\uFCC0', '', ''),
    )),
    ('Kurdish LIGATURE FEH WITH KHAH WITH MEEM', (
        '\u0641\u062E\u0645', ('', '\uFD7D', '', '\uFD7C'),
    )),
    ('Kurdish LIGATURE FEH WITH MEEM', (
        '\u0641\u0645', ('\uFC30', '\uFCC1', '', ''),
    )),
    ('Kurdish LIGATURE FEH WITH MEEM WITH YEH', (
        '\u0641\u0645\u064A', ('', '', '', '\uFDC1'),
    )),
    ('Kurdish LIGATURE FEH WITH YEH', (
        '\u0641\u064A', ('\uFC32', '', '', '\uFC7D'),
    )),
    ('Kurdish LIGATURE GHAIN WITH ALEF MAKSURA', (
        '\u063A\u0649', ('\uFCF9', '', '', '\uFD15'),
    )),
    ('Kurdish LIGATURE GHAIN WITH JEEM', (
        '\u063A\u062C', ('\uFC2B', '\uFCBC', '', ''),
    )),
    ('Kurdish LIGATURE GHAIN WITH MEEM', (
        '\u063A\u0645', ('\uFC2C', '\uFCBD', '', ''),
    )),
    ('Kurdish LIGATURE GHAIN WITH MEEM WITH ALEF MAKSURA', (
        '\u063A\u0645\u0649', ('', '', '', '\uFD7B'),
    )),
    ('Kurdish LIGATURE GHAIN WITH MEEM WITH MEEM', (
        '\u063A\u0645\u0645', ('', '', '', '\uFD79'),
    )),
    ('Kurdish LIGATURE GHAIN WITH MEEM WITH YEH', (
        '\u063A\u0645\u064A', ('', '', '', '\uFD7A'),
    )),
    ('Kurdish LIGATURE GHAIN WITH YEH', (
        '\u063A\u064A', ('\uFCFA', '', '', '\uFD16'),
    )),
    ('Kurdish LIGATURE HAH WITH ALEF MAKSURA', (
        '\u062D\u0649', ('\uFCFF', '', '', '\uFD1B'),
    )),
    ('Kurdish LIGATURE HAH WITH JEEM', (
        '\u062D\u062C', ('\uFC17', '\uFCA9', '', ''),
    )),
    ('Kurdish LIGATURE HAH WITH JEEM WITH YEH', (
        '\u062D\u062C\u064A', ('', '', '', '\uFDBF'),
    )),
    ('Kurdish LIGATURE HAH WITH MEEM', (
        '\u062D\u0645', ('\uFC18', '\uFCAA', '', ''),
    )),
    ('Kurdish LIGATURE HAH WITH MEEM WITH ALEF MAKSURA', (
        '\u062D\u0645\u0649', ('', '', '', '\uFD5B'),
    )),
    ('Kurdish LIGATURE HAH WITH MEEM WITH YEH', (
        '\u062D\u0645\u064A', ('', '', '', '\uFD5A'),
    )),
    ('Kurdish LIGATURE HAH WITH YEH', (
        '\u062D\u064A', ('\uFD00', '', '', '\uFD1C'),
    )),
    ('Kurdish LIGATURE HEH WITH ALEF MAKSURA', (
        '\u0647\u0649', ('\uFC53', '', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH JEEM', (
        '\u0647\u062C', ('\uFC51', '\uFCD7', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH MEEM', (
        '\u0647\u0645', ('\uFC52', '\uFCD8', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH MEEM WITH JEEM', (
        '\u0647\u0645\u062C', ('', '\uFD93', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH MEEM WITH MEEM', (
        '\u0647\u0645\u0645', ('', '\uFD94', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH SUPERSCRIPT ALEF', (
        '\u0647\u0670', ('', '\uFCD9', '', ''),
    )),
    ('Kurdish LIGATURE HEH WITH YEH', (
        '\u0647\u064A', ('\uFC54', '', '', ''),
    )),
    ('Kurdish LIGATURE JEEM WITH ALEF MAKSURA', (
        '\u062C\u0649', ('\uFD01', '', '', '\uFD1D'),
    )),
    ('Kurdish LIGATURE JEEM WITH HAH', (
        '\u062C\u062D', ('\uFC15', '\uFCA7', '', ''),
    )),
    ('Kurdish LIGATURE JEEM WITH HAH WITH ALEF MAKSURA', (
        '\u062C\u062D\u0649', ('', '', '', '\uFDA6'),
    )),
    ('Kurdish LIGATURE JEEM WITH HAH WITH YEH', (
        '\u062C\u062D\u064A', ('', '', '', '\uFDBE'),
    )),
    ('Kurdish LIGATURE JEEM WITH MEEM', (
        '\u062C\u0645', ('\uFC16', '\uFCA8', '', ''),
    )),
    ('Kurdish LIGATURE JEEM WITH MEEM WITH ALEF MAKSURA', (
        '\u062C\u0645\u0649', ('', '', '', '\uFDA7'),
    )),
    ('Kurdish LIGATURE JEEM WITH MEEM WITH HAH', (
        '\u062C\u0645\u062D', ('', '\uFD59', '', '\uFD58'),
    )),
    ('Kurdish LIGATURE JEEM WITH MEEM WITH YEH', (
        '\u062C\u0645\u064A', ('', '', '', '\uFDA5'),
    )),
    ('Kurdish LIGATURE JEEM WITH YEH', (
        '\u062C\u064A', ('\uFD02', '', '', '\uFD1E'),
    )),
    ('Kurdish LIGATURE KAF WITH ALEF', (
        '\u0643\u0627', ('\uFC37', '', '', '\uFC80'),
    )),
    ('Kurdish LIGATURE KAF WITH ALEF MAKSURA', (
        '\u0643\u0649', ('\uFC3D', '', '', '\uFC83'),
    )),
    ('Kurdish LIGATURE KAF WITH HAH', (
        '\u0643\u062D', ('\uFC39', '\uFCC5', '', ''),
    )),
    ('Kurdish LIGATURE KAF WITH JEEM', (
        '\u0643\u062C', ('\uFC38', '\uFCC4', '', ''),
    )),
    ('Kurdish LIGATURE KAF WITH KHAH', (
        '\u0643\u062E', ('\uFC3A', '\uFCC6', '', ''),
    )),
    ('Kurdish LIGATURE KAF WITH LAM', (
        '\u0643\u0644', ('\uFC3B', '\uFCC7', '\uFCEB', '\uFC81'),
    )),
    ('Kurdish LIGATURE KAF WITH MEEM', (
        '\u0643\u0645', ('\uFC3C', '\uFCC8', '\uFCEC', '\uFC82'),
    )),
    ('Kurdish LIGATURE KAF WITH MEEM WITH MEEM', (
        '\u0643\u0645\u0645', ('', '\uFDC3', '', '\uFDBB'),
    )),
    ('Kurdish LIGATURE KAF WITH MEEM WITH YEH', (
        '\u0643\u0645\u064A', ('', '', '', '\uFDB7'),
    )),
    ('Kurdish LIGATURE KAF WITH YEH', (
        '\u0643\u064A', ('\uFC3E', '', '', '\uFC84'),
    )),
    ('Kurdish LIGATURE KHAH WITH ALEF MAKSURA', (
        '\u062E\u0649', ('\uFD03', '', '', '\uFD1F'),
    )),
    ('Kurdish LIGATURE KHAH WITH HAH', (
        '\u062E\u062D', ('\uFC1A', '', '', ''),
    )),
    ('Kurdish LIGATURE KHAH WITH JEEM', (
        '\u062E\u062C', ('\uFC19', '\uFCAB', '', ''),
    )),
    ('Kurdish LIGATURE KHAH WITH MEEM', (
        '\u062E\u0645', ('\uFC1B', '\uFCAC', '', ''),
    )),
    ('Kurdish LIGATURE KHAH WITH YEH', (
        '\u062E\u064A', ('\uFD04', '', '', '\uFD20'),
    )),
    ('Kurdish LIGATURE LAM WITH ALEF', (
        '\u0644\u0627', ('\uFEFB', '', '', '\uFEFC'),
    )),
    ('Kurdish LIGATURE LAM WITH ALEF MAKSURA', (
        '\u0644\u0649', ('\uFC43', '', '', '\uFC86'),
    )),
    ('Kurdish LIGATURE LAM WITH ALEF WITH HAMZA ABOVE', (
        '\u0644\u0623', ('\uFEF7', '', '', '\uFEF8'),
    )),
    ('Kurdish LIGATURE LAM WITH ALEF WITH HAMZA BELOW', (
        '\u0644\u0625', ('\uFEF9', '', '', '\uFEFA'),
    )),
    ('Kurdish LIGATURE LAM WITH ALEF WITH MADDA ABOVE', (
        '\u0644\u0622', ('\uFEF5', '', '', '\uFEF6'),
    )),
    ('Kurdish LIGATURE LAM WITH HAH', (
        '\u0644\u062D', ('\uFC40', '\uFCCA', '', ''),
    )),
    ('Kurdish LIGATURE LAM WITH HAH WITH ALEF MAKSURA', (
        '\u0644\u062D\u0649', ('', '', '', '\uFD82'),
    )),
    ('Kurdish LIGATURE LAM WITH HAH WITH MEEM', (
        '\u0644\u062D\u0645', ('', '\uFDB5', '', '\uFD80'),
    )),
    ('Kurdish LIGATURE LAM WITH HAH WITH YEH', (
        '\u0644\u062D\u064A', ('', '', '', '\uFD81'),
    )),
    ('Kurdish LIGATURE LAM WITH HEH', (
        '\u0644\u0647', ('', '\uFCCD', '', ''),
    )),
    ('Kurdish LIGATURE LAM WITH JEEM', (
        '\u0644\u062C', ('\uFC3F', '\uFCC9', '', ''),
    )),
    ('Kurdish LIGATURE LAM WITH JEEM WITH JEEM', (
        '\u0644\u062C\u062C', ('', '\uFD83', '', '\uFD84'),
    )),
    ('Kurdish LIGATURE LAM WITH JEEM WITH MEEM', (
        '\u0644\u062C\u0645', ('', '\uFDBA', '', '\uFDBC'),
    )),
    ('Kurdish LIGATURE LAM WITH JEEM WITH YEH', (
        '\u0644\u062C\u064A', ('', '', '', '\uFDAC'),
    )),
    ('Kurdish LIGATURE LAM WITH KHAH', (
        '\u0644\u062E', ('\uFC41', '\uFCCB', '', ''),
    )),
    ('Kurdish LIGATURE LAM WITH KHAH WITH MEEM', (
        '\u0644\u062E\u0645', ('', '\uFD86', '', '\uFD85'),
    )),
    ('Kurdish LIGATURE LAM WITH MEEM', (
        '\u0644\u0645', ('\uFC42', '\uFCCC', '\uFCED', '\uFC85'),
    )),
    ('Kurdish LIGATURE LAM WITH MEEM WITH HAH', (
        '\u0644\u0645\u062D', ('', '\uFD88', '', '\uFD87'),
    )),
    ('Kurdish LIGATURE LAM WITH MEEM WITH YEH', (
        '\u0644\u0645\u064A', ('', '', '', '\uFDAD'),
    )),
    ('Kurdish LIGATURE LAM WITH YEH', (
        '\u0644\u064A', ('\uFC44', '', '', '\uFC87'),
    )),
    ('Kurdish LIGATURE MEEM WITH ALEF', (
        '\u0645\u0627', ('', '', '', '\uFC88'),
    )),
    ('Kurdish LIGATURE MEEM WITH ALEF MAKSURA', (
        '\u0645\u0649', ('\uFC49', '', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH HAH', (
        '\u0645\u062D', ('\uFC46', '\uFCCF', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH HAH WITH JEEM', (
        '\u0645\u062D\u062C', ('', '\uFD89', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH HAH WITH MEEM', (
        '\u0645\u062D\u0645', ('', '\uFD8A', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH HAH WITH YEH', (
        '\u0645\u062D\u064A', ('', '', '', '\uFD8B'),
    )),
    ('Kurdish LIGATURE MEEM WITH JEEM', (
        '\u0645\u062C', ('\uFC45', '\uFCCE', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH JEEM WITH HAH', (
        '\u0645\u062C\u062D', ('', '\uFD8C', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH JEEM WITH KHAH', (
        '\u0645\u062C\u062E', ('', '\uFD92', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH JEEM WITH MEEM', (
        '\u0645\u062C\u0645', ('', '\uFD8D', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH JEEM WITH YEH', (
        '\u0645\u062C\u064A', ('', '', '', '\uFDC0'),
    )),
    ('Kurdish LIGATURE MEEM WITH KHAH', (
        '\u0645\u062E', ('\uFC47', '\uFCD0', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH KHAH WITH JEEM', (
        '\u0645\u062E\u062C', ('', '\uFD8E', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH KHAH WITH MEEM', (
        '\u0645\u062E\u0645', ('', '\uFD8F', '', ''),
    )),
    ('Kurdish LIGATURE MEEM WITH KHAH WITH YEH', (
        '\u0645\u062E\u064A', ('', '', '', '\uFDB9'),
    )),
    ('Kurdish LIGATURE MEEM WITH MEEM', (
        '\u0645\u0645', ('\uFC48', '\uFCD1', '', '\uFC89'),
    )),
    ('Kurdish LIGATURE MEEM WITH MEEM WITH YEH', (
        '\u0645\u0645\u064A', ('', '', '', '\uFDB1'),
    )),
    ('Kurdish LIGATURE MEEM WITH YEH', (
        '\u0645\u064A', ('\uFC4A', '', '', ''),
    )),
    ('Kurdish LIGATURE NOON WITH ALEF MAKSURA', (
        '\u0646\u0649', ('\uFC4F', '', '', '\uFC8E'),
    )),
    ('Kurdish LIGATURE NOON WITH HAH', (
        '\u0646\u062D', ('\uFC4C', '\uFCD3', '', ''),
    )),
    ('Kurdish LIGATURE NOON WITH HAH WITH ALEF MAKSURA', (
        '\u0646\u062D\u0649', ('', '', '', '\uFD96'),
    )),
    ('Kurdish LIGATURE NOON WITH HAH WITH MEEM', (
        '\u0646\u062D\u0645', ('', '\uFD95', '', ''),
    )),
    ('Kurdish LIGATURE NOON WITH HAH WITH YEH', (
        '\u0646\u062D\u064A', ('', '', '', '\uFDB3'),
    )),
    ('Kurdish LIGATURE NOON WITH HEH', (
        '\u0646\u0647', ('', '\uFCD6', '\uFCEF', ''),
    )),
    ('Kurdish LIGATURE NOON WITH JEEM', (
        '\u0646\u062C', ('\uFC4B', '\uFCD2', '', ''),
    )),
    ('Kurdish LIGATURE NOON WITH JEEM WITH ALEF MAKSURA', (
        '\u0646\u062C\u0649', ('', '', '', '\uFD99'),
    )),
    ('Kurdish LIGATURE NOON WITH JEEM WITH HAH', (
        '\u0646\u062C\u062D', ('', '\uFDB8', '', '\uFDBD'),
    )),
    ('Kurdish LIGATURE NOON WITH JEEM WITH MEEM', (
        '\u0646\u062C\u0645', ('', '\uFD98', '', '\uFD97'),
    )),
    ('Kurdish LIGATURE NOON WITH JEEM WITH YEH', (
        '\u0646\u062C\u064A', ('', '', '', '\uFDC7'),
    )),
    ('Kurdish LIGATURE NOON WITH KHAH', (
        '\u0646\u062E', ('\uFC4D', '\uFCD4', '', ''),
    )),
    ('Kurdish LIGATURE NOON WITH MEEM', (
        '\u0646\u0645', ('\uFC4E', '\uFCD5', '\uFCEE', '\uFC8C'),
    )),
    ('Kurdish LIGATURE NOON WITH MEEM WITH ALEF MAKSURA', (
        '\u0646\u0645\u0649', ('', '', '', '\uFD9B'),
    )),
    ('Kurdish LIGATURE NOON WITH MEEM WITH YEH', (
        '\u0646\u0645\u064A', ('', '', '', '\uFD9A'),
    )),
    ('Kurdish LIGATURE NOON WITH NOON', (
        '\u0646\u0646', ('', '', '', '\uFC8D'),
    )),
    ('Kurdish LIGATURE NOON WITH REH', (
        '\u0646\u0631', ('', '', '', '\uFC8A'),
    )),
    ('Kurdish LIGATURE NOON WITH YEH', (
        '\u0646\u064A', ('\uFC50', '', '', '\uFC8F'),
    )),
    ('Kurdish LIGATURE NOON WITH ZAIN', (
        '\u0646\u0632', ('', '', '', '\uFC8B'),
    )),
    ('Kurdish LIGATURE QAF WITH ALEF MAKSURA', (
        '\u0642\u0649', ('\uFC35', '', '', '\uFC7E'),
    )),
    ('Kurdish LIGATURE QAF WITH HAH', (
        '\u0642\u062D', ('\uFC33', '\uFCC2', '', ''),
    )),
    ('Kurdish LIGATURE QAF WITH MEEM', (
        '\u0642\u0645', ('\uFC34', '\uFCC3', '', ''),
    )),
    ('Kurdish LIGATURE QAF WITH MEEM WITH HAH', (
        '\u0642\u0645\u062D', ('', '\uFDB4', '', '\uFD7E'),
    )),
    ('Kurdish LIGATURE QAF WITH MEEM WITH MEEM', (
        '\u0642\u0645\u0645', ('', '', '', '\uFD7F'),
    )),
    ('Kurdish LIGATURE QAF WITH MEEM WITH YEH', (
        '\u0642\u0645\u064A', ('', '', '', '\uFDB2'),
    )),
    ('Kurdish LIGATURE QAF WITH YEH', (
        '\u0642\u064A', ('\uFC36', '', '', '\uFC7F'),
    )),
    ('Kurdish LIGATURE QALA USED AS KORANIC STOP SIGN', (
        '\u0642\u0644\u06D2', ('\uFDF1', '', '', ''),
    )),
    ('Kurdish LIGATURE REH WITH SUPERSCRIPT ALEF', (
        '\u0631\u0670', ('\uFC5C', '', '', ''),
    )),
    ('Kurdish LIGATURE SAD WITH ALEF MAKSURA', (
        '\u0635\u0649', ('\uFD05', '', '', '\uFD21'),
    )),
    ('Kurdish LIGATURE SAD WITH HAH', (
        '\u0635\u062D', ('\uFC20', '\uFCB1', '', ''),
    )),
    ('Kurdish LIGATURE SAD WITH HAH WITH HAH', (
        '\u0635\u062D\u062D', ('', '\uFD65', '', '\uFD64'),
    )),
    ('Kurdish LIGATURE SAD WITH HAH WITH YEH', (
        '\u0635\u062D\u064A', ('', '', '', '\uFDA9'),
    )),
    ('Kurdish LIGATURE SAD WITH KHAH', (
        '\u0635\u062E', ('', '\uFCB2', '', ''),
    )),
    ('Kurdish LIGATURE SAD WITH MEEM', (
        '\u0635\u0645', ('\uFC21', '\uFCB3', '', ''),
    )),
    ('Kurdish LIGATURE SAD WITH MEEM WITH MEEM', (
        '\u0635\u0645\u0645', ('', '\uFDC5', '', '\uFD66'),
    )),
    ('Kurdish LIGATURE SAD WITH REH', (
        '\u0635\u0631', ('\uFD0F', '', '', '\uFD2B'),
    )),
    ('Kurdish LIGATURE SAD WITH YEH', (
        '\u0635\u064A', ('\uFD06', '', '', '\uFD22'),
    )),
    ('Kurdish LIGATURE SALLA USED AS KORANIC STOP SIGN', (
        '\u0635\u0644\u06D2', ('\uFDF0', '', '', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH ALEF MAKSURA', (
        '\u0633\u0649', ('\uFCFB', '', '', '\uFD17'),
    )),
    ('Kurdish LIGATURE SEEN WITH HAH', (
        '\u0633\u062D', ('\uFC1D', '\uFCAE', '\uFD35', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH HAH WITH JEEM', (
        '\u0633\u062D\u062C', ('', '\uFD5C', '', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH HEH', (
        '\u0633\u0647', ('', '\uFD31', '\uFCE8', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH JEEM', (
        '\u0633\u062C', ('\uFC1C', '\uFCAD', '\uFD34', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH JEEM WITH ALEF MAKSURA', (
        '\u0633\u062C\u0649', ('', '', '', '\uFD5E'),
    )),
    ('Kurdish LIGATURE SEEN WITH JEEM WITH HAH', (
        '\u0633\u062C\u062D', ('', '\uFD5D', '', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH KHAH', (
        '\u0633\u062E', ('\uFC1E', '\uFCAF', '\uFD36', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH KHAH WITH ALEF MAKSURA', (
        '\u0633\u062E\u0649', ('', '', '', '\uFDA8'),
    )),
    ('Kurdish LIGATURE SEEN WITH KHAH WITH YEH', (
        '\u0633\u062E\u064A', ('', '', '', '\uFDC6'),
    )),
    ('Kurdish LIGATURE SEEN WITH MEEM', (
        '\u0633\u0645', ('\uFC1F', '\uFCB0', '\uFCE7', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH MEEM WITH HAH', (
        '\u0633\u0645\u062D', ('', '\uFD60', '', '\uFD5F'),
    )),
    ('Kurdish LIGATURE SEEN WITH MEEM WITH JEEM', (
        '\u0633\u0645\u062C', ('', '\uFD61', '', ''),
    )),
    ('Kurdish LIGATURE SEEN WITH MEEM WITH MEEM', (
        '\u0633\u0645\u0645', ('', '\uFD63', '', '\uFD62'),
    )),
    ('Kurdish LIGATURE SEEN WITH REH', (
        '\u0633\u0631', ('\uFD0E', '', '', '\uFD2A'),
    )),
    ('Kurdish LIGATURE SEEN WITH YEH', (
        '\u0633\u064A', ('\uFCFC', '', '', '\uFD18'),
    )),

    # Kurdish ligatures with Shadda, the order of characters doesn't matter
    ('Kurdish LIGATURE SHADDA WITH DAMMATAN ISOLATED FORM', (
        '(?:\u064C\u0651|\u0651\u064C)',

        ('\uFC5E', '\uFC5E', '\uFC5E', '\uFC5E'),
    )),
    ('Kurdish LIGATURE SHADDA WITH KASRATAN ISOLATED FORM', (
        '(?:\u064D\u0651|\u0651\u064D)',

        ('\uFC5F', '\uFC5F', '\uFC5F', '\uFC5F'),
    )),
    ('Kurdish LIGATURE SHADDA WITH FATHA ISOLATED FORM', (
        '(?:\u064E\u0651|\u0651\u064E)',

        ('\uFC60', '\uFC60', '\uFC60', '\uFC60'),
    )),
    ('Kurdish LIGATURE SHADDA WITH DAMMA ISOLATED FORM', (
        '(?:\u064F\u0651|\u0651\u064F)',

        ('\uFC61', '\uFC61', '\uFC61', '\uFC61'),
    )),
    ('Kurdish LIGATURE SHADDA WITH KASRA ISOLATED FORM', (
        '(?:\u0650\u0651|\u0651\u0650)',

        ('\uFC62', '\uFC62', '\uFC62', '\uFC62'),
    )),
    ('Kurdish LIGATURE SHADDA WITH SUPERSCRIPT ALEF', (
        '(?:\u0651\u0670|\u0670\u0651)', ('\uFC63', '', '', ''),
    )),

    # There is a special case when they are with Tatweel
    ('Kurdish LIGATURE SHADDA WITH FATHA MEDIAL FORM', (
        '\u0640(?:\u064E\u0651|\u0651\u064E)',

        ('\uFCF2', '\uFCF2', '\uFCF2', '\uFCF2'),
    )),
    ('Kurdish LIGATURE SHADDA WITH DAMMA MEDIAL FORM', (
        '\u0640(?:\u064F\u0651|\u0651\u064F)',

        ('\uFCF3', '\uFCF3', '\uFCF3', '\uFCF3'),
    )),
    ('Kurdish LIGATURE SHADDA WITH KASRA MEDIAL FORM', (
        '\u0640(?:\u0650\u0651|\u0651\u0650)',

        ('\uFCF4', '\uFCF4', '\uFCF4', '\uFCF4'),
    )),

    # Repeated with different keys to be backward compatible
    ('Kurdish LIGATURE SHADDA WITH FATHA', (
        '\u0640(?:\u064E\u0651|\u0651\u064E)',

        ('\uFCF2', '\uFCF2', '\uFCF2', '\uFCF2'),
    )),
    ('Kurdish LIGATURE SHADDA WITH DAMMA', (
        '\u0640(?:\u064F\u0651|\u0651\u064F)',

        ('\uFCF3', '\uFCF3', '\uFCF3', '\uFCF3'),
    )),
    ('Kurdish LIGATURE SHADDA WITH KASRA', (
        '\u0640(?:\u0650\u0651|\u0651\u0650)',

        ('\uFCF4', '\uFCF4', '\uFCF4', '\uFCF4'),
    )),

    ('Kurdish LIGATURE SHEEN WITH ALEF MAKSURA', (
        '\u0634\u0649', ('\uFCFD', '', '', '\uFD19'),
    )),
    ('Kurdish LIGATURE SHEEN WITH HAH', (
        '\u0634\u062D', ('\uFD0A', '\uFD2E', '\uFD38', '\uFD26'),
    )),
    ('Kurdish LIGATURE SHEEN WITH HAH WITH MEEM', (
        '\u0634\u062D\u0645', ('', '\uFD68', '', '\uFD67'),
    )),
    ('Kurdish LIGATURE SHEEN WITH HAH WITH YEH', (
        '\u0634\u062D\u064A', ('', '', '', '\uFDAA'),
    )),
    ('Kurdish LIGATURE SHEEN WITH HEH', (
        '\u0634\u0647', ('', '\uFD32', '\uFCEA', ''),
    )),
    ('Kurdish LIGATURE SHEEN WITH JEEM', (
        '\u0634\u062C', ('\uFD09', '\uFD2D', '\uFD37', '\uFD25'),
    )),
    ('Kurdish LIGATURE SHEEN WITH JEEM WITH YEH', (
        '\u0634\u062C\u064A', ('', '', '', '\uFD69'),
    )),
    ('Kurdish LIGATURE SHEEN WITH KHAH', (
        '\u0634\u062E', ('\uFD0B', '\uFD2F', '\uFD39', '\uFD27'),
    )),
    ('Kurdish LIGATURE SHEEN WITH MEEM', (
        '\u0634\u0645', ('\uFD0C', '\uFD30', '\uFCE9', '\uFD28'),
    )),
    ('Kurdish LIGATURE SHEEN WITH MEEM WITH KHAH', (
        '\u0634\u0645\u062E', ('', '\uFD6B', '', '\uFD6A'),
    )),
    ('Kurdish LIGATURE SHEEN WITH MEEM WITH MEEM', (
        '\u0634\u0645\u0645', ('', '\uFD6D', '', '\uFD6C'),
    )),
    ('Kurdish LIGATURE SHEEN WITH REH', (
        '\u0634\u0631', ('\uFD0D', '', '', '\uFD29'),
    )),
    ('Kurdish LIGATURE SHEEN WITH YEH', (
        '\u0634\u064A', ('\uFCFE', '', '', '\uFD1A'),
    )),
    ('Kurdish LIGATURE TAH WITH ALEF MAKSURA', (
        '\u0637\u0649', ('\uFCF5', '', '', '\uFD11'),
    )),
    ('Kurdish LIGATURE TAH WITH HAH', (
        '\u0637\u062D', ('\uFC26', '\uFCB8', '', ''),
    )),
    ('Kurdish LIGATURE TAH WITH MEEM', (
        '\u0637\u0645', ('\uFC27', '\uFD33', '\uFD3A', ''),
    )),
    ('Kurdish LIGATURE TAH WITH MEEM WITH HAH', (
        '\u0637\u0645\u062D', ('', '\uFD72', '', '\uFD71'),
    )),
    ('Kurdish LIGATURE TAH WITH MEEM WITH MEEM', (
        '\u0637\u0645\u0645', ('', '\uFD73', '', ''),
    )),
    ('Kurdish LIGATURE TAH WITH MEEM WITH YEH', (
        '\u0637\u0645\u064A', ('', '', '', '\uFD74'),
    )),
    ('Kurdish LIGATURE TAH WITH YEH', (
        '\u0637\u064A', ('\uFCF6', '', '', '\uFD12'),
    )),
    ('Kurdish LIGATURE TEH WITH ALEF MAKSURA', (
        '\u062A\u0649', ('\uFC0F', '', '', '\uFC74'),
    )),
    ('Kurdish LIGATURE TEH WITH HAH', (
        '\u062A\u062D', ('\uFC0C', '\uFCA2', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH HAH WITH JEEM', (
        '\u062A\u062D\u062C', ('', '\uFD52', '', '\uFD51'),
    )),
    ('Kurdish LIGATURE TEH WITH HAH WITH MEEM', (
        '\u062A\u062D\u0645', ('', '\uFD53', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH HEH', (
        '\u062A\u0647', ('', '\uFCA5', '\uFCE4', ''),
    )),
    ('Kurdish LIGATURE TEH WITH JEEM', (
        '\u062A\u062C', ('\uFC0B', '\uFCA1', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH JEEM WITH ALEF MAKSURA', (
        '\u062A\u062C\u0649', ('', '', '', '\uFDA0'),
    )),
    ('Kurdish LIGATURE TEH WITH JEEM WITH MEEM', (
        '\u062A\u062C\u0645', ('', '\uFD50', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH JEEM WITH YEH', (
        '\u062A\u062C\u064A', ('', '', '', '\uFD9F'),
    )),
    ('Kurdish LIGATURE TEH WITH KHAH', (
        '\u062A\u062E', ('\uFC0D', '\uFCA3', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH KHAH WITH ALEF MAKSURA', (
        '\u062A\u062E\u0649', ('', '', '', '\uFDA2'),
    )),
    ('Kurdish LIGATURE TEH WITH KHAH WITH MEEM', (
        '\u062A\u062E\u0645', ('', '\uFD54', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH KHAH WITH YEH', (
        '\u062A\u062E\u064A', ('', '', '', '\uFDA1'),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM', (
        '\u062A\u0645', ('\uFC0E', '\uFCA4', '\uFCE3', '\uFC72'),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM WITH ALEF MAKSURA', (
        '\u062A\u0645\u0649', ('', '', '', '\uFDA4'),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM WITH HAH', (
        '\u062A\u0645\u062D', ('', '\uFD56', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM WITH JEEM', (
        '\u062A\u0645\u062C', ('', '\uFD55', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM WITH KHAH', (
        '\u062A\u0645\u062E', ('', '\uFD57', '', ''),
    )),
    ('Kurdish LIGATURE TEH WITH MEEM WITH YEH', (
        '\u062A\u0645\u064A', ('', '', '', '\uFDA3'),
    )),
    ('Kurdish LIGATURE TEH WITH NOON', (
        '\u062A\u0646', ('', '', '', '\uFC73'),
    )),
    ('Kurdish LIGATURE TEH WITH REH', (
        '\u062A\u0631', ('', '', '', '\uFC70'),
    )),
    ('Kurdish LIGATURE TEH WITH YEH', (
        '\u062A\u064A', ('\uFC10', '', '', '\uFC75'),
    )),
    ('Kurdish LIGATURE TEH WITH ZAIN', (
        '\u062A\u0632', ('', '', '', '\uFC71'),
    )),
    ('Kurdish LIGATURE THAL WITH SUPERSCRIPT ALEF', (
        '\u0630\u0670', ('\uFC5B', '', '', ''),
    )),
    ('Kurdish LIGATURE THEH WITH ALEF MAKSURA', (
        '\u062B\u0649', ('\uFC13', '', '', '\uFC7A'),
    )),
    ('Kurdish LIGATURE THEH WITH HEH', (
        '\u062B\u0647', ('', '', '\uFCE6', ''),
    )),
    ('Kurdish LIGATURE THEH WITH JEEM', (
        '\u062B\u062C', ('\uFC11', '', '', ''),
    )),
    ('Kurdish LIGATURE THEH WITH MEEM', (
        '\u062B\u0645', ('\uFC12', '\uFCA6', '\uFCE5', '\uFC78'),
    )),
    ('Kurdish LIGATURE THEH WITH NOON', (
        '\u062B\u0646', ('', '', '', '\uFC79'),
    )),
    ('Kurdish LIGATURE THEH WITH REH', (
        '\u062B\u0631', ('', '', '', '\uFC76'),
    )),
    ('Kurdish LIGATURE THEH WITH YEH', (
        '\u062B\u064A', ('\uFC14', '', '', '\uFC7B'),
    )),
    ('Kurdish LIGATURE THEH WITH ZAIN', (
        '\u062B\u0632', ('', '', '', '\uFC77'),
    )),
    ('Kurdish LIGATURE UIGHUR KIRGHIZ YEH WITH HAMZA ABOVE WITH ALEF MAKSURA', (
        '\u0626\u0649', ('\uFBF9', '\uFBFB', '', '\uFBFA'),
    )),
    ('Kurdish LIGATURE YEH WITH ALEF MAKSURA', (
        '\u064A\u0649', ('\uFC59', '', '', '\uFC95'),
    )),
    ('Kurdish LIGATURE YEH WITH HAH', (
        '\u064A\u062D', ('\uFC56', '\uFCDB', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH HAH WITH YEH', (
        '\u064A\u062D\u064A', ('', '', '', '\uFDAE'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH AE', (
        '\u0626\u06D5', ('\uFBEC', '', '', '\uFBED'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ALEF', (
        '\u0626\u0627', ('\uFBEA', '', '', '\uFBEB'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA', (
        '\u0626\u0649', ('\uFC03', '', '', '\uFC68'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH E', (
        '\u0626\u06D0', ('\uFBF6', '\uFBF8', '', '\uFBF7'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH HAH', (
        '\u0626\u062D', ('\uFC01', '\uFC98', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH HEH', (
        '\u0626\u0647', ('', '\uFC9B', '\uFCE0', ''),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH JEEM', (
        '\u0626\u062C', ('\uFC00', '\uFC97', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH KHAH', (
        '\u0626\u062E', ('', '\uFC99', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH MEEM', (
        '\u0626\u0645', ('\uFC02', '\uFC9A', '\uFCDF', '\uFC66'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH NOON', (
        '\u0626\u0646', ('', '', '', '\uFC67'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH OE', (
        '\u0626\u06C6', ('\uFBF2', '', '', '\uFBF3'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH REH', (
        '\u0626\u0631', ('', '', '', '\uFC64'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH U', (
        '\u0626\u06C7', ('\uFBF0', '', '', '\uFBF1'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH WAW', (
        '\u0626\u0648', ('\uFBEE', '', '', '\uFBEF'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH YEH', (
        '\u0626\u064A', ('\uFC04', '', '', '\uFC69'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH YU', (
        '\u0626\u06C8', ('\uFBF4', '', '', '\uFBF5'),
    )),
    ('Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ZAIN', (
        '\u0626\u0632', ('', '', '', '\uFC65'),
    )),
    ('Kurdish LIGATURE YEH WITH HEH', (
        '\u064A\u0647', ('', '\uFCDE', '\uFCF1', ''),
    )),
    ('Kurdish LIGATURE YEH WITH JEEM', (
        '\u064A\u062C', ('\uFC55', '\uFCDA', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH JEEM WITH YEH', (
        '\u064A\u062C\u064A', ('', '', '', '\uFDAF'),
    )),
    ('Kurdish LIGATURE YEH WITH KHAH', (
        '\u064A\u062E', ('\uFC57', '\uFCDC', '', ''),
    )),
    ('Kurdish LIGATURE YEH WITH MEEM', (
        '\u064A\u0645', ('\uFC58', '\uFCDD', '\uFCF0', '\uFC93'),
    )),
    ('Kurdish LIGATURE YEH WITH MEEM WITH MEEM', (
        '\u064A\u0645\u0645', ('', '\uFD9D', '', '\uFD9C'),
    )),
    ('Kurdish LIGATURE YEH WITH MEEM WITH YEH', (
        '\u064A\u0645\u064A', ('', '', '', '\uFDB0'),
    )),
    ('Kurdish LIGATURE YEH WITH NOON', (
        '\u064A\u0646', ('', '', '', '\uFC94'),
    )),
    ('Kurdish LIGATURE YEH WITH REH', (
        '\u064A\u0631', ('', '', '', '\uFC91'),
    )),
    ('Kurdish LIGATURE YEH WITH YEH', (
        '\u064A\u064A', ('\uFC5A', '', '', '\uFC96'),
    )),
    ('Kurdish LIGATURE YEH WITH ZAIN', (
        '\u064A\u0632', ('', '', '', '\uFC92'),
    )),
    ('Kurdish LIGATURE ZAH WITH MEEM', (
        '\u0638\u0645', ('\uFC28', '\uFCB9', '\uFD3B', ''),
    )),
)

LIGATURES = tuple(chain(SENTENCES_LIGATURES, WORDS_LIGATURES, LETTERS_LIGATURES))
