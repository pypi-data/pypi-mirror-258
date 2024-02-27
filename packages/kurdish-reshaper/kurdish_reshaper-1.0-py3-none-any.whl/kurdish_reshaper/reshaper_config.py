

import os

from configparser import ConfigParser

from .letters import (UNSHAPED, ISOLATED, LETTERS_Kurdish)
from .ligatures import (SENTENCES_LIGATURES,
                        WORDS_LIGATURES,
                        LETTERS_LIGATURES)

try:
    from fontTools.ttLib import TTFont
    with_font_config = True
except ImportError:
    with_font_config = False

ENABLE_NO_LIGATURES = 0b000
ENABLE_SENTENCES_LIGATURES = 0b001
ENABLE_WORDS_LIGATURES = 0b010
ENABLE_LETTERS_LIGATURES = 0b100
ENABLE_ALL_LIGATURES = 0b111

default_config = {
    # Supported languages are: [Kurdish, KurdishV2, Kurdish]
    # More languages might be supported soon.
    # `Kurdish` is default and recommended to work in most of the cases and
    # supports (Kurdish, Urdu and Farsi)
    # `KurdishV2` is only to be used with certain font that you run into missing
    # chars `Kurdish` if you are using Kurdish Sarchia font is recommended,
    # work with both unicode and classic Kurdish-Kurdish keybouard
    'language': 'Kurdish',

    # Whether to delete the Harakat (Tashkeel) before reshaping or not.
    'delete_harakat': True,

    # Whether to shift the Harakat (Tashkeel) one position so they appear
    # correctly when string is reversed
    'shift_harakat_position': False,

    # Whether to delete the Tatweel (U+0640) before reshaping or not.
    'delete_tatweel': False,

    # Whether to support ZWJ (U+200D) or not.
    'support_zwj': True,

    # Use unshaped form instead of isolated form.
    'use_unshaped_instead_of_isolated': False,

    # Whether to use ligatures or not.
    # Serves as a shortcut to disable all ligatures.
    'support_ligatures': True,

    # When `support_ligatures` is enabled.
    # Separate ligatures configuration take precedence over it.
    # When `support_ligatures` is disabled,
    # separate ligatures configurations are ignored.

    # ------------------- Begin: Ligatures Configurations ------------------ #

    # Sentences (Enabled on top)
    'Kurdish LIGATURE BISMILLAH AR-RAHMAN AR-RAHEEM': False,
    'Kurdish LIGATURE JALLAJALALOUHOU': False,
    'Kurdish LIGATURE SALLALLAHOU ALAYHE WASALLAM': False,

    # Words (Enabled on top)
    'Kurdish LIGATURE ALLAH': True,
    'Kurdish LIGATURE AKBAR': False,
    'Kurdish LIGATURE ALAYHE': False,
    'Kurdish LIGATURE MOHAMMAD': False,
    'Kurdish LIGATURE RASOUL': False,
    'Kurdish LIGATURE SALAM': False,
    'Kurdish LIGATURE SALLA': False,
    'Kurdish LIGATURE WASALLAM': False,
    'RIAL SIGN': False,

    # Letters (Enabled on top)
    'Kurdish LIGATURE LAM WITH ALEF': True,
    'Kurdish LIGATURE LAM WITH ALEF WITH HAMZA ABOVE': True,
    'Kurdish LIGATURE LAM WITH ALEF WITH HAMZA BELOW': True,
    'Kurdish LIGATURE LAM WITH ALEF WITH MADDA ABOVE': True,
    'Kurdish LIGATURE AIN WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE AIN WITH JEEM': False,
    'Kurdish LIGATURE AIN WITH JEEM WITH MEEM': False,
    'Kurdish LIGATURE AIN WITH MEEM': False,
    'Kurdish LIGATURE AIN WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE AIN WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE AIN WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE AIN WITH YEH': False,
    'Kurdish LIGATURE ALEF MAKSURA WITH SUPERSCRIPT ALEF': False,
    'Kurdish LIGATURE ALEF WITH FATHATAN': False,
    'Kurdish LIGATURE BEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE BEH WITH HAH': False,
    'Kurdish LIGATURE BEH WITH HAH WITH YEH': False,
    'Kurdish LIGATURE BEH WITH HEH': False,
    'Kurdish LIGATURE BEH WITH JEEM': False,
    'Kurdish LIGATURE BEH WITH KHAH': False,
    'Kurdish LIGATURE BEH WITH KHAH WITH YEH': False,
    'Kurdish LIGATURE BEH WITH MEEM': False,
    'Kurdish LIGATURE BEH WITH NOON': False,
    'Kurdish LIGATURE BEH WITH REH': False,
    'Kurdish LIGATURE BEH WITH YEH': False,
    'Kurdish LIGATURE BEH WITH ZAIN': False,
    'Kurdish LIGATURE DAD WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE DAD WITH HAH': False,
    'Kurdish LIGATURE DAD WITH HAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE DAD WITH HAH WITH YEH': False,
    'Kurdish LIGATURE DAD WITH JEEM': False,
    'Kurdish LIGATURE DAD WITH KHAH': False,
    'Kurdish LIGATURE DAD WITH KHAH WITH MEEM': False,
    'Kurdish LIGATURE DAD WITH MEEM': False,
    'Kurdish LIGATURE DAD WITH REH': False,
    'Kurdish LIGATURE DAD WITH YEH': False,
    'Kurdish LIGATURE FEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE FEH WITH HAH': False,
    'Kurdish LIGATURE FEH WITH JEEM': False,
    'Kurdish LIGATURE FEH WITH KHAH': False,
    'Kurdish LIGATURE FEH WITH KHAH WITH MEEM': False,
    'Kurdish LIGATURE FEH WITH MEEM': False,
    'Kurdish LIGATURE FEH WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE FEH WITH YEH': False,
    'Kurdish LIGATURE GHAIN WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE GHAIN WITH JEEM': False,
    'Kurdish LIGATURE GHAIN WITH MEEM': False,
    'Kurdish LIGATURE GHAIN WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE GHAIN WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE GHAIN WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE GHAIN WITH YEH': False,
    'Kurdish LIGATURE HAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE HAH WITH JEEM': False,
    'Kurdish LIGATURE HAH WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE HAH WITH MEEM': False,
    'Kurdish LIGATURE HAH WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE HAH WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE HAH WITH YEH': False,
    'Kurdish LIGATURE HEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE HEH WITH JEEM': False,
    'Kurdish LIGATURE HEH WITH MEEM': False,
    'Kurdish LIGATURE HEH WITH MEEM WITH JEEM': False,
    'Kurdish LIGATURE HEH WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE HEH WITH SUPERSCRIPT ALEF': False,
    'Kurdish LIGATURE HEH WITH YEH': False,
    'Kurdish LIGATURE JEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE JEEM WITH HAH': False,
    'Kurdish LIGATURE JEEM WITH HAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE JEEM WITH HAH WITH YEH': False,
    'Kurdish LIGATURE JEEM WITH MEEM': False,
    'Kurdish LIGATURE JEEM WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE JEEM WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE JEEM WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE JEEM WITH YEH': False,
    'Kurdish LIGATURE KAF WITH ALEF': False,
    'Kurdish LIGATURE KAF WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE KAF WITH HAH': False,
    'Kurdish LIGATURE KAF WITH JEEM': False,
    'Kurdish LIGATURE KAF WITH KHAH': False,
    'Kurdish LIGATURE KAF WITH LAM': False,
    'Kurdish LIGATURE KAF WITH MEEM': False,
    'Kurdish LIGATURE KAF WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE KAF WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE KAF WITH YEH': False,
    'Kurdish LIGATURE KHAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE KHAH WITH HAH': False,
    'Kurdish LIGATURE KHAH WITH JEEM': False,
    'Kurdish LIGATURE KHAH WITH MEEM': False,
    'Kurdish LIGATURE KHAH WITH YEH': False,
    'Kurdish LIGATURE LAM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE LAM WITH HAH': False,
    'Kurdish LIGATURE LAM WITH HAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE LAM WITH HAH WITH MEEM': False,
    'Kurdish LIGATURE LAM WITH HAH WITH YEH': False,
    'Kurdish LIGATURE LAM WITH HEH': False,
    'Kurdish LIGATURE LAM WITH JEEM': False,
    'Kurdish LIGATURE LAM WITH JEEM WITH JEEM': False,
    'Kurdish LIGATURE LAM WITH JEEM WITH MEEM': False,
    'Kurdish LIGATURE LAM WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE LAM WITH KHAH': False,
    'Kurdish LIGATURE LAM WITH KHAH WITH MEEM': False,
    'Kurdish LIGATURE LAM WITH MEEM': False,
    'Kurdish LIGATURE LAM WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE LAM WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE LAM WITH YEH': False,
    'Kurdish LIGATURE MEEM WITH ALEF': False,
    'Kurdish LIGATURE MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE MEEM WITH HAH': False,
    'Kurdish LIGATURE MEEM WITH HAH WITH JEEM': False,
    'Kurdish LIGATURE MEEM WITH HAH WITH MEEM': False,
    'Kurdish LIGATURE MEEM WITH HAH WITH YEH': False,
    'Kurdish LIGATURE MEEM WITH JEEM': False,
    'Kurdish LIGATURE MEEM WITH JEEM WITH HAH': False,
    'Kurdish LIGATURE MEEM WITH JEEM WITH KHAH': False,
    'Kurdish LIGATURE MEEM WITH JEEM WITH MEEM': False,
    'Kurdish LIGATURE MEEM WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE MEEM WITH KHAH': False,
    'Kurdish LIGATURE MEEM WITH KHAH WITH JEEM': False,
    'Kurdish LIGATURE MEEM WITH KHAH WITH MEEM': False,
    'Kurdish LIGATURE MEEM WITH KHAH WITH YEH': False,
    'Kurdish LIGATURE MEEM WITH MEEM': False,
    'Kurdish LIGATURE MEEM WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE MEEM WITH YEH': False,
    'Kurdish LIGATURE NOON WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE NOON WITH HAH': False,
    'Kurdish LIGATURE NOON WITH HAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE NOON WITH HAH WITH MEEM': False,
    'Kurdish LIGATURE NOON WITH HAH WITH YEH': False,
    'Kurdish LIGATURE NOON WITH HEH': False,
    'Kurdish LIGATURE NOON WITH JEEM': False,
    'Kurdish LIGATURE NOON WITH JEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE NOON WITH JEEM WITH HAH': False,
    'Kurdish LIGATURE NOON WITH JEEM WITH MEEM': False,
    'Kurdish LIGATURE NOON WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE NOON WITH KHAH': False,
    'Kurdish LIGATURE NOON WITH MEEM': False,
    'Kurdish LIGATURE NOON WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE NOON WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE NOON WITH NOON': False,
    'Kurdish LIGATURE NOON WITH REH': False,
    'Kurdish LIGATURE NOON WITH YEH': False,
    'Kurdish LIGATURE NOON WITH ZAIN': False,
    'Kurdish LIGATURE QAF WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE QAF WITH HAH': False,
    'Kurdish LIGATURE QAF WITH MEEM': False,
    'Kurdish LIGATURE QAF WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE QAF WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE QAF WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE QAF WITH YEH': False,
    'Kurdish LIGATURE QALA USED AS KORANIC STOP SIGN': False,
    'Kurdish LIGATURE REH WITH SUPERSCRIPT ALEF': False,
    'Kurdish LIGATURE SAD WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE SAD WITH HAH': False,
    'Kurdish LIGATURE SAD WITH HAH WITH HAH': False,
    'Kurdish LIGATURE SAD WITH HAH WITH YEH': False,
    'Kurdish LIGATURE SAD WITH KHAH': False,
    'Kurdish LIGATURE SAD WITH MEEM': False,
    'Kurdish LIGATURE SAD WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE SAD WITH REH': False,
    'Kurdish LIGATURE SAD WITH YEH': False,
    'Kurdish LIGATURE SALLA USED AS KORANIC STOP SIGN': False,
    'Kurdish LIGATURE SEEN WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE SEEN WITH HAH': False,
    'Kurdish LIGATURE SEEN WITH HAH WITH JEEM': False,
    'Kurdish LIGATURE SEEN WITH HEH': False,
    'Kurdish LIGATURE SEEN WITH JEEM': False,
    'Kurdish LIGATURE SEEN WITH JEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE SEEN WITH JEEM WITH HAH': False,
    'Kurdish LIGATURE SEEN WITH KHAH': False,
    'Kurdish LIGATURE SEEN WITH KHAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE SEEN WITH KHAH WITH YEH': False,
    'Kurdish LIGATURE SEEN WITH MEEM': False,
    'Kurdish LIGATURE SEEN WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE SEEN WITH MEEM WITH JEEM': False,
    'Kurdish LIGATURE SEEN WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE SEEN WITH REH': False,
    'Kurdish LIGATURE SEEN WITH YEH': False,
    'Kurdish LIGATURE SHADDA WITH DAMMA': False,
    'Kurdish LIGATURE SHADDA WITH DAMMA ISOLATED FORM': False,
    'Kurdish LIGATURE SHADDA WITH DAMMA MEDIAL FORM': False,
    'Kurdish LIGATURE SHADDA WITH DAMMATAN ISOLATED FORM': False,
    'Kurdish LIGATURE SHADDA WITH FATHA': False,
    'Kurdish LIGATURE SHADDA WITH FATHA ISOLATED FORM': False,
    'Kurdish LIGATURE SHADDA WITH FATHA MEDIAL FORM': False,
    'Kurdish LIGATURE SHADDA WITH KASRA': False,
    'Kurdish LIGATURE SHADDA WITH KASRA ISOLATED FORM': False,
    'Kurdish LIGATURE SHADDA WITH KASRA MEDIAL FORM': False,
    'Kurdish LIGATURE SHADDA WITH KASRATAN ISOLATED FORM': False,
    'Kurdish LIGATURE SHADDA WITH SUPERSCRIPT ALEF': False,
    'Kurdish LIGATURE SHADDA WITH SUPERSCRIPT ALEF ISOLATED FORM': False,
    'Kurdish LIGATURE SHEEN WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE SHEEN WITH HAH': False,
    'Kurdish LIGATURE SHEEN WITH HAH WITH MEEM': False,
    'Kurdish LIGATURE SHEEN WITH HAH WITH YEH': False,
    'Kurdish LIGATURE SHEEN WITH HEH': False,
    'Kurdish LIGATURE SHEEN WITH JEEM': False,
    'Kurdish LIGATURE SHEEN WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE SHEEN WITH KHAH': False,
    'Kurdish LIGATURE SHEEN WITH MEEM': False,
    'Kurdish LIGATURE SHEEN WITH MEEM WITH KHAH': False,
    'Kurdish LIGATURE SHEEN WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE SHEEN WITH REH': False,
    'Kurdish LIGATURE SHEEN WITH YEH': False,
    'Kurdish LIGATURE TAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE TAH WITH HAH': False,
    'Kurdish LIGATURE TAH WITH MEEM': False,
    'Kurdish LIGATURE TAH WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE TAH WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE TAH WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE TAH WITH YEH': False,
    'Kurdish LIGATURE TEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE TEH WITH HAH': False,
    'Kurdish LIGATURE TEH WITH HAH WITH JEEM': False,
    'Kurdish LIGATURE TEH WITH HAH WITH MEEM': False,
    'Kurdish LIGATURE TEH WITH HEH': False,
    'Kurdish LIGATURE TEH WITH JEEM': False,
    'Kurdish LIGATURE TEH WITH JEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE TEH WITH JEEM WITH MEEM': False,
    'Kurdish LIGATURE TEH WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE TEH WITH KHAH': False,
    'Kurdish LIGATURE TEH WITH KHAH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE TEH WITH KHAH WITH MEEM': False,
    'Kurdish LIGATURE TEH WITH KHAH WITH YEH': False,
    'Kurdish LIGATURE TEH WITH MEEM': False,
    'Kurdish LIGATURE TEH WITH MEEM WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE TEH WITH MEEM WITH HAH': False,
    'Kurdish LIGATURE TEH WITH MEEM WITH JEEM': False,
    'Kurdish LIGATURE TEH WITH MEEM WITH KHAH': False,
    'Kurdish LIGATURE TEH WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE TEH WITH NOON': False,
    'Kurdish LIGATURE TEH WITH REH': False,
    'Kurdish LIGATURE TEH WITH YEH': False,
    'Kurdish LIGATURE TEH WITH ZAIN': False,
    'Kurdish LIGATURE THAL WITH SUPERSCRIPT ALEF': False,
    'Kurdish LIGATURE THEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE THEH WITH HEH': False,
    'Kurdish LIGATURE THEH WITH JEEM': False,
    'Kurdish LIGATURE THEH WITH MEEM': False,
    'Kurdish LIGATURE THEH WITH NOON': False,
    'Kurdish LIGATURE THEH WITH REH': False,
    'Kurdish LIGATURE THEH WITH YEH': False,
    'Kurdish LIGATURE THEH WITH ZAIN': False,
    'Kurdish LIGATURE UIGHUR KIRGHIZ YEH WITH HAMZA ABOVE WITH ALEF MAKSURA': False,  # noqa
    'Kurdish LIGATURE YEH WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE YEH WITH HAH': False,
    'Kurdish LIGATURE YEH WITH HAH WITH YEH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH AE': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ALEF': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH E': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH HAH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH HEH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH JEEM': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH KHAH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH MEEM': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH NOON': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH OE': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH REH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH U': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH WAW': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH YEH': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH YU': False,
    'Kurdish LIGATURE YEH WITH HAMZA ABOVE WITH ZAIN': False,
    'Kurdish LIGATURE YEH WITH HEH': False,
    'Kurdish LIGATURE YEH WITH JEEM': False,
    'Kurdish LIGATURE YEH WITH JEEM WITH YEH': False,
    'Kurdish LIGATURE YEH WITH KHAH': False,
    'Kurdish LIGATURE YEH WITH MEEM': False,
    'Kurdish LIGATURE YEH WITH MEEM WITH MEEM': False,
    'Kurdish LIGATURE YEH WITH MEEM WITH YEH': False,
    'Kurdish LIGATURE YEH WITH NOON': False,
    'Kurdish LIGATURE YEH WITH REH': False,
    'Kurdish LIGATURE YEH WITH YEH': False,
    'Kurdish LIGATURE YEH WITH ZAIN': False,
    'Kurdish LIGATURE ZAH WITH MEEM': False,
    # -------------------- End: Ligatures Configurations ------------------- #
}


def auto_config(configuration=None, configuration_file=None):
    loaded_from_envvar = False

    configuration_parser = ConfigParser()
    configuration_parser.read_dict({
        'KurdishReshaper': default_config
    })

    if not configuration_file:
        configuration_file = os.getenv(
            'PYTHON_Kurdish_RESHAPER_CONFIGURATION_FILE'
        )
        if configuration_file:
            loaded_from_envvar = True

    if configuration_file:
        if not os.path.exists(configuration_file):
            raise Exception(
                'Configuration file {} not found{}.'.format(
                    configuration_file,
                    loaded_from_envvar and (
                        ' it is set in your environment variable ' +
                        'PYTHON_Kurdish_RESHAPER_CONFIGURATION_FILE'
                    ) or ''
                )
            )
        configuration_parser.read((configuration_file,))

    if configuration:
        configuration_parser.read_dict({
            'KurdishReshaper': configuration
        })

    if 'KurdishReshaper' not in configuration_parser:
        raise ValueError(
            'Invalid configuration: '
            'A section with the name KurdishReshaper was not found'
        )

    return configuration_parser['KurdishReshaper']


def config_for_true_type_font(font_file_path,
                              ligatures_config=ENABLE_ALL_LIGATURES):
    if not with_font_config:
        raise Exception('fonttools not installed, ' +
                        'install it then rerun this.\n' +
                        '$ pip install Kurdish-teshaper[with-fonttools]')
    if not font_file_path or not os.path.exists(font_file_path):
        raise Exception('Invalid path to font file')
    ttfont = TTFont(font_file_path)
    has_isolated = True
    for k, v in LETTERS_Kurdish.items():
        for table in ttfont['cmap'].tables:
            if ord(v[ISOLATED]) in table.cmap:
                break
        else:
            has_isolated = False
            break

    configuration = {
        'use_unshaped_instead_of_isolated': not has_isolated,
    }

    def process_ligatures(ligatures):
        for ligature in ligatures:
            forms = list(filter(lambda form: form != '', ligature[1][1]))
            n = len(forms)
            for form in forms:
                for table in ttfont['cmap'].tables:
                    if ord(form) in table.cmap:
                        n -= 1
                        break
            configuration[ligature[0]] = (n == 0)

    if ENABLE_SENTENCES_LIGATURES & ligatures_config:
        process_ligatures(SENTENCES_LIGATURES)

    if ENABLE_WORDS_LIGATURES & ligatures_config:
        process_ligatures(WORDS_LIGATURES)

    if ENABLE_LETTERS_LIGATURES & ligatures_config:
        process_ligatures(LETTERS_LIGATURES)

    return configuration
