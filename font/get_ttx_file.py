import glob
import time
import numpy as np
import cv2
from datetime import datetime


dict_hex_to_name = {'x22': 'quotedbl', 'x25': 'percent', 'x26': 'ampersand', 'x27': 'quotesingle', 'x28': 'parenleft', 'x29': 'parenright', 'x2c': 'comma', 'x2d': 'hyphen', 'x2e': 'period', 'x2f': 'slash', 'x30': 'zero', 'x31': 'one', 'x32': 'two', 'x33': 'three', 'x34': 'four', 'x35': 'five', 'x36': 'six', 'x37': 'seven', 'x38': 'eight', 'x39': 'nine', 'x3a': 'colon', 'x3d': 'equal', 'x3f': 'question', 'x41': 'A', 'x42': 'B', 'x43': 'C', 'x44': 'D', 'x45': 'E', 'x46': 'F', 'x47': 'G', 'x48': 'H', 'x49': 'I', 'x4a': 'J', 'x4b': 'K', 'x4c': 'L', 'x4d': 'M', 'x4e': 'N', 'x4f': 'O', 'x50': 'P', 'x51': 'Q', 'x52': 'R', 'x53': 'S', 'x54': 'T', 'x55': 'U', 'x56': 'V', 'x57': 'W', 'x58': 'X', 'x59': 'Y', 'x5a': 'Z', 'x61': 'a', 'x62': 'b', 'x63': 'c', 'x64': 'd', 'x65': 'e', 'x66': 'f', 'x67': 'g', 'x68': 'h', 'x69': 'i', 'x6a': 'j', 'x6b': 'k', 'x6c': 'l', 'x6d': 'm', 'x6e': 'n', 'x6f': 'o', 'x70': 'p', 'x71': 'q', 'x72': 'r', 'x73': 's', 'x74': 't', 'x75': 'u', 'x76': 'v', 'x77': 'w', 'x78': 'x', 'x79': 'y', 'x7a': 'z', 'x21': 'exclam', 'x23': 'numbersign', 'x24': 'dollar', 'x2a': 'asterisk', 'x2b': 'plus', 'x3b': 'semicolon', 'x3c': 'less', 'x3e': 'greater', 'x40': 'at', 'x5b': 'bracketleft', 'x5c': 'backslash', 'x5d': 'bracketright', 'x5e': 'carat', 'x5f': 'underscore', 'x60': 'grave', 'x7b': 'braceleft', 'x7c': 'pipe', 'x7d': 'braceright', 'x7e': 'tilde'}


dict_hex_to_char = {'x22': '"', 'x25': '%', 'x26': '&', 'x27': "'", 'x28': '(', 'x29': ')', 'x2c': ',', 'x2d': '-', 'x2e': '.', 'x2f': '/', 'x30': '0', 'x31': '1', 'x32': '2', 'x33': '3', 'x34': '4', 'x35': '5', 'x36': '6', 'x37': '7', 'x38': '8', 'x39': '9', 'x3a': ':', 'x3d': '=', 'x3f': '?', 'x41': 'A', 'x42': 'B', 'x43': 'C', 'x44': 'D', 'x45': 'E', 'x46': 'F', 'x47': 'G', 'x48': 'H', 'x49': 'I', 'x4a': 'J', 'x4b': 'K', 'x4c': 'L', 'x4d': 'M', 'x4e': 'N', 'x4f': 'O', 'x50': 'P', 'x51': 'Q', 'x52': 'R', 'x53': 'S', 'x54': 'T', 'x55': 'U', 'x56': 'V', 'x57': 'W', 'x58': 'X', 'x59': 'Y', 'x5a': 'Z', 'x61': 'a', 'x62': 'b', 'x63': 'c', 'x64': 'd', 'x65': 'e', 'x66': 'f', 'x67': 'g', 'x68': 'h', 'x69': 'i', 'x6a': 'j', 'x6b': 'k', 'x6c': 'l', 'x6d': 'm', 'x6e': 'n', 'x6f': 'o', 'x70': 'p', 'x71': 'q', 'x72': 'r', 'x73': 's', 'x74': 't', 'x75': 'u', 'x76': 'v', 'x77': 'w', 'x78': 'x', 'x79': 'y', 'x7a': 'z', 'x21': '!', 'x23': '#', 'x24': '$', 'x2a': '*', 'x2b': '+', 'x3b': ';', 'x3c': '<', 'x3e': '>', 'x40': '@', 'x5b': '[', 'x5c': '\\', 'x5d': ']', 'x5e': '^', 'x5f': '_', 'x60': '`', 'x7b': '{', 'x7c': '|', 'x7d': '}', 'x7e': '~'}


dict_hex_to_unicode_name = {'x22': 'QUOTATION MARK', 'x25': 'PERCENT SIGN', 'x26': 'AMPERSAND', 'x27': 'APOSTROPHE', 'x28': 'LEFT PARENTHESIS', 'x29': 'RIGHT PARENTHESIS', 'x2c': 'COMMA', 'x2d': 'HYPHEN-MINUS', 'x2e': 'FULL STOP', 'x2f': 'SOLIDUS', 'x30': 'DIGIT ZERO', 'x31': 'DIGIT ONE', 'x32': 'DIGIT TWO', 'x33': 'DIGIT THREE', 'x34': 'DIGIT FOUR', 'x35': 'DIGIT FIVE', 'x36': 'DIGIT SIX', 'x37': 'DIGIT SEVEN', 'x38': 'DIGIT EIGHT', 'x39': 'DIGIT NINE', 'x3a': 'COLON', 'x3d': 'EQUALS SIGN', 'x3f': 'QUESTION MARK', 'x41': 'LATIN CAPITAL LETTER A', 'x42': 'LATIN CAPITAL LETTER B', 'x43': 'LATIN CAPITAL LETTER C', 'x44': 'LATIN CAPITAL LETTER D', 'x45': 'LATIN CAPITAL LETTER E', 'x46': 'LATIN CAPITAL LETTER F', 'x47': 'LATIN CAPITAL LETTER G', 'x48': 'LATIN CAPITAL LETTER H', 'x49': 'LATIN CAPITAL LETTER I', 'x4a': 'LATIN CAPITAL LETTER J', 'x4b': 'LATIN CAPITAL LETTER K', 'x4c': 'LATIN CAPITAL LETTER L', 'x4d': 'LATIN CAPITAL LETTER M', 'x4e': 'LATIN CAPITAL LETTER N', 'x4f': 'LATIN CAPITAL LETTER O', 'x50': 'LATIN CAPITAL LETTER P', 'x51': 'LATIN CAPITAL LETTER Q', 'x52': 'LATIN CAPITAL LETTER R', 'x53': 'LATIN CAPITAL LETTER S', 'x54': 'LATIN CAPITAL LETTER T', 'x55': 'LATIN CAPITAL LETTER U', 'x56': 'LATIN CAPITAL LETTER V', 'x57': 'LATIN CAPITAL LETTER W', 'x58': 'LATIN CAPITAL LETTER X', 'x59': 'LATIN CAPITAL LETTER Y', 'x5a': 'LATIN CAPITAL LETTER Z', 'x61': 'LATIN SMALL LETTER A', 'x62': 'LATIN SMALL LETTER B', 'x63': 'LATIN SMALL LETTER C', 'x64': 'LATIN SMALL LETTER D', 'x65': 'LATIN SMALL LETTER E', 'x66': 'LATIN SMALL LETTER F', 'x67': 'LATIN SMALL LETTER G', 'x68': 'LATIN SMALL LETTER H', 'x69': 'LATIN SMALL LETTER I', 'x6a': 'LATIN SMALL LETTER J', 'x6b': 'LATIN SMALL LETTER K', 'x6c': 'LATIN SMALL LETTER L', 'x6d': 'LATIN SMALL LETTER M', 'x6e': 'LATIN SMALL LETTER N', 'x6f': 'LATIN SMALL LETTER O', 'x70': 'LATIN SMALL LETTER P', 'x71': 'LATIN SMALL LETTER Q', 'x72': 'LATIN SMALL LETTER R', 'x73': 'LATIN SMALL LETTER S', 'x74': 'LATIN SMALL LETTER T', 'x75': 'LATIN SMALL LETTER U', 'x76': 'LATIN SMALL LETTER V', 'x77': 'LATIN SMALL LETTER W', 'x78': 'LATIN SMALL LETTER X', 'x79': 'LATIN SMALL LETTER Y', 'x7a': 'LATIN SMALL LETTER Z', 'x21': 'EXCLAMATION MARK', 'x23': 'NUMBER SIGN', 'x24': 'DOLLAR SIGN', 'x2a': 'ASTERISK', 'x2b': 'PLUS SIGN', 'x3b': 'SEMICOLON', 'x3c': 'LESS-THAN SIGN', 'x3e': 'GREATER-THAN SIGN', 'x40': 'COMMERCIAL AT', 'x5b': 'LEFT SQUARE BRACKET', 'x5c': 'REVERSE SOLIDUS', 'x5d': 'RIGHT SQUARE BRACKET', 'x5e': 'CIRCUMFLEX ACCENT', 'x5f': 'LOW LINE', 'x60': 'GRAVE ACCENT', 'x7b': 'LEFT CURLY BRACKET', 'x7c': 'VERTICAL LINE', 'x7d': 'RIGHT CURLY BRACKET', 'x7e': 'TILDE'}


dict_uppercase_characters_hex_values = {'x41': 'A', 'x42': 'B', 'x43': 'C', 'x44': 'D', 'x45': 'E', 'x46': 'F', 'x47': 'G', 'x48': 'H', 'x49': 'I', 'x4a': 'J', 'x4b': 'K', 'x4c': 'L', 'x4d': 'M', 'x4e': 'N', 'x4f': 'O', 'x50': 'P', 'x51': 'Q', 'x52': 'R', 'x53': 'S', 'x54': 'T', 'x55': 'U', 'x56': 'V', 'x57': 'W', 'x58': 'X', 'x59': 'Y', 'x5a': 'Z'}

dict_lowercase_characters_hex_values = {'x61': 'a', 'x62': 'b', 'x63': 'c', 'x64': 'd', 'x65': 'e', 'x66': 'f', 'x67': 'g', 'x68': 'h', 'x69': 'i', 'x6a': 'j', 'x6b': 'k', 'x6c': 'l', 'x6d': 'm', 'x6e': 'n', 'x6f': 'o', 'x70': 'p', 'x71': 'q', 'x72': 'r', 'x73': 's', 'x74': 't', 'x75': 'u', 'x76': 'v', 'x77': 'w', 'x78': 'x', 'x79': 'y', 'x7a': 'z'}

dict_numbers_hex_values = {'x30': '0', 'x31': '1', 'x32': '2', 'x33': '3', 'x34': '4', 'x35': '5', 'x36': '6', 'x37': '7', 'x38': '8', 'x39': '9'}

dict_symbols_hex_values = {'x22': '"', 'x25': '%', 'x26': '&', 'x27': "'", 'x28': '(', 'x29': ')', 'x2c': ',', 'x2d': '-', 'x2e': '.', 'x2f': '/', 'x3a': ':', 'x3d': '=', 'x3f': '?', 'x21': '!', 'x23': '#', 'x24': '$', 'x2a': '*', 'x2b': '+', 'x3b': ';', 'x3c': '<', 'x3e': '>', 'x40': '@', 'x5b': '[', 'x5c': '\\', 'x5d': ']', 'x5e': '^', 'x5f': '_', 'x60': '`', 'x7b': '{', 'x7c': '|', 'x7d': '}', 'x7e': '~'}


def generate_ttx_file(folder_path, name_font):

    global_xmin = 0
    global_ymin = 0
    global_xmax = 0
    global_ymax = 0
    global_advance_width_max = 0  # max width of all glyph defined in hmtx table
    global_max_points = 0         # max points in a glyph ( sum of all contour points )
    global_max_contours = 0       # max number of contours in a glyph
    global_xavg_char_width = 0    # average of sum of all advance width defined in hmtx table
    global_sx_height = 0          # The distance between the baseline and the approximate height of non-ascending lowercase letters
                                # measured in FUnits
    global_scap_height = 0        # The distance between the baseline and the approximate height of uppercase letters measured in
                                # FUnits
    font_name = name_font
    font_style = "Regular"
    font_creator = "HARSHIT GARG"
    font_creation_date = datetime.today().strftime('%Y-%m-%d')           # YYYY-MM-DD FORMAT
    font_creation_date = font_creation_date.split('-')
    font_creation_date = font_creation_date[2] + '-' + font_creation_date[1] + '-' + font_creation_date[0]   # DD-MM-YYYY FORMAT


    prefix = folder_path + '/'
    ext = 'png'
    image_files = {}
    glob_pat = "%s*.%s" % (prefix, ext)
    leading = len(prefix)
    trailing = len(ext) + 1

    lowercase = ""
    uppercase = ""
    numbers = ""
    symbols = ""

    for image_file in glob.glob(glob_pat):
        name = image_file[leading:-trailing]
        image_files[name] = image_file
        
        if name in dict_uppercase_characters_hex_values:
            uppercase += dict_uppercase_characters_hex_values[name]
        elif name in dict_lowercase_characters_hex_values:
            lowercase += dict_lowercase_characters_hex_values[name]
        elif name in dict_numbers_hex_values:
            numbers += dict_numbers_hex_values[name]
        elif name in dict_symbols_hex_values:
            symbols += dict_symbols_hex_values[name]

    user_char_count = len(image_files)

    # HEADER LINES AND START OF TTFONT TAG
    ttx_file = open(folder_path + '/' + font_name + '.ttx','w')
    starting_part_1 = '<?xml version="1.0" encoding="UTF-8"?>\n<ttFont sfntVersion="\\x00\\x01\\x00\\x00" ttLibVersion="4.10">' + '\n\n'


    # START OF GLYPHORDER TABLE
    glyphorder_part_1 = '  <GlyphOrder>\n    <!-- The "id" attribute is only for humans; it is ignored when parsed. -->\n    <GlyphID id="0" name=".notdef"/>\n    <GlyphID id="1" name=".null"/>\n    <GlyphID id="2" name="nonmarkingreturn"/>\n    <GlyphID id="3" name="CR"/>\n    <GlyphID id="4" name="space"/>\n'


    glyphorder_part_2 = ''
    i = 5
    for key in image_files.keys():
        glyphorder_part_2 += '    <GlyphID id="' + str(i) + '" name="' + dict_hex_to_name[key] + '"/>\n'
        i += 1

    glyphorder_part_3 = '    <GlyphID id="' + str(i) + '" name="nbsp"/>\n  </GlyphOrder>\n\n'
    # END OF GLYPHORDER TABLE



    # START OF HEAD TABLE
    head_part_1 = '  <head>\n    <!-- Most of this table will be recalculated by the compiler -->\n    <tableVersion value="1.0"/>\n    <fontRevision value="1.0"/>\n    <checkSumAdjustment value="0xbac9824e"/>\n    <magicNumber value="0x5f0f3cf5"/>\n    <flags value="00000000 00001011"/>\n    <unitsPerEm value="1000"/>\n    <created value="' + time.ctime() + '"/>\n    <modified value="' + time.ctime() + '"/>\n    '


    head_part_2 = '<xMin value="' + str(global_xmin) + '"/>\n    <yMin value="' + str(global_ymin) + '"/>\n    <xMax value="' + str(global_xmax) + '"/>\n    <yMax value="' + str(global_ymax) + '"/>'


    head_part_3 = '\n    <macStyle value="00000000 00000000"/>\n    <lowestRecPPEM value="8"/>\n    <fontDirectionHint value="2"/>\n    <indexToLocFormat value="0"/>\n    <glyphDataFormat value="0"/>\n  </head>\n\n'

    # END OF HEAD TABLE



    # START OF HHEA TABLE
    hhea_part_1 = '  <hhea>\n    <tableVersion value="0x00010000"/>\n    '


    hhea_part_2 = '<ascent value="' + str(global_ymax) + '"/>\n    <descent value="' + str(global_ymin) + '"/>\n    <lineGap value="90"/>\n    <advanceWidthMax value="' + str(global_advance_width_max) + '"/>\n    <minLeftSideBearing value="0"/>\n    <minRightSideBearing value="0"/>\n    <xMaxExtent value="' + str(global_xmax) + '"/>'


    hhea_part_3 = '\n    <caretSlopeRise value="1"/>\n    <caretSlopeRun value="0"/>\n    <caretOffset value="0"/>\n    <reserved0 value="0"/>\n    <reserved1 value="0"/>\n    <reserved2 value="0"/>\n    <reserved3 value="0"/>\n    <metricDataFormat value="0"/>\n    <numberOfHMetrics value="' + str(i+1) + '"/>\n  </hhea>\n\n'

    # END OF HHEA TABLE




    # START OF MAXP TABLE
    maxp_part_1 = '  <maxp>\n    <!-- Most of this table will be recalculated by the compiler -->\n    <tableVersion value="0x10000"/>\n    <numGlyphs value="' + str(i+1) + '"/>\n    '


    maxp_part_2 = '<maxPoints value="' + str(global_max_points) + '"/>\n    <maxContours value="' + str(global_max_contours) + '"/>'


    maxp_part_3 = '\n    <maxCompositePoints value="0"/>\n    <maxCompositeContours value="0"/>\n    <maxZones value="2"/>\n    <maxTwilightPoints value="0"/>\n    <maxStorage value="1"/>\n    <maxFunctionDefs value="1"/>\n    <maxInstructionDefs value="0"/>\n    <maxStackElements value="64"/>\n    <maxSizeOfInstructions value="0"/>\n    <maxComponentElements value="0"/>\n    <maxComponentDepth value="0"/>\n  </maxp>\n\n'

    # END OF MAXP TABLE




    # START OF OS_2 TABLE
    os_2_part_1 = '  <OS_2>\n    <!-- The fields "usFirstCharIndex" and "usLastCharIndex"\n         will be recalculated by the compiler -->\n    <version value="4"/>\n    '


    os_2_part_2 = '<xAvgCharWidth value="' + str(global_xavg_char_width) + '"/>'


    os_2_part_3 = '\n    <usWeightClass value="400"/>\n    <usWidthClass value="5"/>\n    <fsType value="00000000 00000000"/>\n    <ySubscriptXSize value="650"/>\n    <ySubscriptYSize value="700"/>\n    <ySubscriptXOffset value="0"/>\n    <ySubscriptYOffset value="140"/>\n    <ySuperscriptXSize value="650"/>\n    <ySuperscriptYSize value="700"/>\n    <ySuperscriptXOffset value="0"/>\n    <ySuperscriptYOffset value="480"/>\n    <yStrikeoutSize value="49"/>\n    <yStrikeoutPosition value="258"/>\n    <sFamilyClass value="0"/>\n    <panose>\n      <bFamilyType value="2"/>\n      <bSerifStyle value="0"/>\n      <bWeight value="5"/>\n      <bProportion value="3"/>\n      <bContrast value="0"/>\n      <bStrokeVariation value="0"/>\n      <bArmStyle value="0"/>\n      <bLetterForm value="0"/>\n      <bMidline value="0"/>\n      <bXHeight value="0"/>\n    </panose>\n    <ulUnicodeRange1 value="00000000 00000000 00000000 00000011"/>\n    <ulUnicodeRange2 value="00000000 00000000 00000000 00000000"/>\n    <ulUnicodeRange3 value="00000000 00000000 00000000 00000000"/>\n    <ulUnicodeRange4 value="00000000 00000000 00000000 00000000"/>\n    <achVendID value="CLGR"/>\n    <fsSelection value="00000000 01000000"/>\n    <usFirstCharIndex value="0"/>\n    <usLastCharIndex value="160"/>\n    <sTypoAscender value="800"/>\n    <sTypoDescender value="-200"/>\n    <sTypoLineGap value="90"/>\n    '


    os_2_part_4 = '<usWinAscent value="' + str(global_ymax) + '"/>\n    <usWinDescent value="' + str(global_ymin) + '"/>\n    <ulCodePageRange1 value="00000000 00000000 00000000 00000001"/>\n    <ulCodePageRange2 value="00000000 00000000 00000000 00000000"/>\n    <sxHeight value="' + str(global_sx_height) + '"/>\n    <sCapHeight value="' + str(global_scap_height) + '"/>\n    <usDefaultChar value="0"/>\n    <usBreakChar value="32"/>\n    <usMaxContext value="1"/>\n  </OS_2>\n\n'

    # END OF OS_2 TABLE



    # START OF HMTX TABLE
    hmtx_part_1 = '  <hmtx>\n    <mtx name=".notdef" width="364" lsb="33"/>\n    <mtx name=".null" width="250" lsb="0"/>\n    <mtx name="CR" width="250" lsb="0"/>\n    <mtx name="nbsp" width="250" lsb="0"/>\n    <mtx name="nonmarkingreturn" width="333" lsb="0"/>\n    <mtx name="space" width="250" lsb="0"/>\n'

    global_xavg_char_width = 364 + 250 + 250 + 250 + 333 + 250

    # it will be completed during contour generation
    hmtx_part_2 = ''

    hmtx_part_3 = '  </hmtx>\n\n'
    # END OF HMTX TABLE



    # START OF CMAP TABLE
    cmap_part_1 = '  <cmap>\n    <tableVersion version="0"/>\n    <cmap_format_4 platformID="0" platEncID="3" language="0">\n      <map code="0x0" name=".null"/><!-- ???? -->\n      <map code="0xd" name="CR"/><!-- ???? -->\n      <map code="0x20" name="space"/><!-- SPACE -->\n'


    cmap_part_2 = ''
    for key in image_files.keys():
        cmap_part_2 += '      <map code="0' + key + '" name="' + dict_hex_to_name[key] + '"/><!-- ' + dict_hex_to_unicode_name[key] + ' -->\n'


    cmap_part_3 = '      <map code="0xa0" name="nbsp"/><!-- NO-BREAK SPACE -->\n      </cmap_format_4>\n    <cmap_format_0 platformID="1" platEncID="0" language="0">\n      <map code="0x0" name=".null"/>\n      <map code="0x8" name=".null"/>\n      <map code="0x9" name="nonmarkingreturn"/>\n      <map code="0xd" name="CR"/>\n      <map code="0x1d" name=".null"/>\n      <map code="0x20" name="space"/>\n'


    cmap_part_4 = ''
    for key in image_files.keys():
        cmap_part_4 += '      <map code="0' + key + '" name="' + dict_hex_to_name[key] + '"/>\n'


    cmap_part_5 = '      <map code="0xca" name="nbsp"/>\n    </cmap_format_0>\n    <cmap_format_4 platformID="3" platEncID="1" language="0">\n      <map code="0x0" name=".null"/><!-- ???? -->\n      <map code="0xd" name="CR"/><!-- ???? -->\n      <map code="0x20" name="space"/><!-- SPACE -->\n'


    cmap_part_6 = cmap_part_2


    cmap_part_7 = '      <map code="0xa0" name="nbsp"/><!-- NO-BREAK SPACE -->\n    </cmap_format_4>\n  </cmap>\n\n'

    # END OF CMAP TABLE




    # START OF PREP TABLE
    prep_part_1 = '  <prep>\n    <assembly>\n      PUSHW[ ]	/* 1 value pushed */\n      511\n      SCANCTRL[ ]	/* ScanConversionControl */\n      PUSHB[ ]	/* 1 value pushed */\n      4\n      SCANTYPE[ ]	/* ScanType */\n    </assembly>\n  </prep>\n\n'
    # END OF PREP TABLE



    # START OF CVT TABLE
    cvt_part_1 = '  <cvt>\n    <cv index="0" value="33"/>\n    <cv index="1" value="633"/>\n  </cvt>\n\n'
    # END OF CVT TABLE



    # START OF LOCA TABLE
    loca_part_1 = '  <loca>\n    <!-- The "loca" table will be calculated by the compiler -->\n  </loca>'
    # END OF LOCA TABLE




    # START OF GLYF TABLE
    glyf_part_1 = '  <glyf>\n\n    <!-- The xMin, yMin, xMax and yMax values\n         will be recalculated by the compiler. -->\n\n    <TTGlyph name=".notdef" xMin="33" yMin="0" xMax="298" yMax="666">\n      <contour>\n        <pt x="33" y="0" on="1"/>\n        <pt x="33" y="666" on="1"/>\n        <pt x="298" y="666" on="1"/>\n        <pt x="298" y="0" on="1"/>\n      </contour>\n      <contour>\n        <pt x="66" y="33" on="1"/>\n        <pt x="265" y="33" on="1"/>\n        <pt x="265" y="633" on="1"/>\n        <pt x="66" y="633" on="1"/>\n      </contour>\n      <instructions/>\n    </TTGlyph>\n\n    <TTGlyph name=".null"/><!-- contains no outline data -->\n\n    <TTGlyph name="CR"/><!-- contains no outline data -->\n\n    <TTGlyph name="nbsp"/><!-- contains no outline data -->\n\n    <TTGlyph name="nonmarkingreturn"/><!-- contains no outline data -->\n\n    <TTGlyph name="space"/><!-- contains no outline data -->\n\n'


    global_xmin = 33
    global_ymin = 0
    global_xmax = 298
    global_ymax = 666


    glyf_part_2 = ''
    for key in image_files.keys():
        xmin = 1000000
        ymin = 1000000
        xmax = 0
        ymax = 0

        # temp_1 need to be updated later when all contours are generated
        temp_1 = '    <TTGlyph name="' + dict_hex_to_name[key] + '" xMin="' + str(xmin) + '" yMin="' + str(ymin) + '" xMax="' + str(xmax) + '" yMax="' + str(ymax) + '">\n'

        img = cv2.imread(image_files[key])
        img = cv2.flip(img, 0)
        dim = (1000, 1300)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


        # converting from BGR to HSV color space
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        # Range for lower red
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Range for upper range
        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        mask2 = cv2.inRange(hsv,lower_red,upper_red)

        # Generating the final mask to detect red color
        mask1 = mask1+mask2

        img = mask1


        # Converting image to a binary image
        # ( black and white only image).
        _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

        # Detecting contours in image.
        contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Going through every contours found in the image.
        temp_2 = ''
        points_in_glyph = 0
        contours_in_glyph = len(contours)

        # for calculating the value of x_shift_to_right by considering all contours for a glyph
        glyph_minx = 1000000
        for cnt in contours :
            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])[0]
            glyph_minx = min(glyph_minx, leftmost)

        x_shift_to_right = glyph_minx - 50

        for cnt in contours :
            temp_2 += '      <contour>\n'
            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])[0]
            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])[0]
            topmost = tuple(cnt[cnt[:,:,1].argmin()][0])[1]
            bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])[1]

            leftmost = leftmost - x_shift_to_right
            rightmost = rightmost - x_shift_to_right

            xmin = min(xmin, leftmost)
            xmax = max(xmax, rightmost)
            ymin = min(ymin, topmost)
            ymax = max(ymax, bottommost)

            approx = cv2.approxPolyDP(cnt, 0.0025 * cv2.arcLength(cnt, True), True)
            n = approx.ravel()
            i = 0

            points_in_glyph += len(n)//2

            for j in n:
                if(i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    temp_2 += '        <pt x="' + str(x - x_shift_to_right) + '" y="' + str(y) + '" on="1"/>\n'

                i = i + 1
            temp_2 += '      </contour>\n'

        temp_2 += '      <instructions/>\n    </TTGlyph>\n\n'

        hmtx_part_2 += '    <mtx name="' + dict_hex_to_name[key] + '" width="' + str(xmin + xmax) + '" lsb="' + str(xmin) + '"/>\n'

        global_xavg_char_width += (xmin + xmax)

        global_xmin = min(global_xmin, xmin)
        global_xmax = max(global_xmax, xmax)
        global_ymin = min(global_ymin, ymin)
        global_ymax = max(global_ymax, ymax)
        global_max_points = max(global_max_points, points_in_glyph)
        global_max_contours = max(global_max_contours, contours_in_glyph)
        global_advance_width_max = max(global_advance_width_max, xmin + xmax)

        if key in dict_uppercase_characters_hex_values:
            global_scap_height = max(global_scap_height, ymax)

        if key in dict_lowercase_characters_hex_values:
            global_sx_height = max(global_sx_height, ymax)

        # updated temp_1 string
        temp_1 = '    <TTGlyph name="' + dict_hex_to_name[key] + '" xMin="' + str(xmin) + '" yMin="' + str(ymin) + '" xMax="' + str(xmax) + '" yMax="' + str(ymax) + '">\n'

        glyf_part_2 += temp_1 + temp_2


    glyf_part_2 += '  </glyf>\n\n'
    global_xavg_char_width = (global_xavg_char_width)//(user_char_count + 6) + 1

    # END OF GLYF TABLE



    # START OF NAME TABLE
    name_part_1 = '  <name>\n    <namerecord nameID="1" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      ' + font_name + '\n    </namerecord>\n    <namerecord nameID="2" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      ' + font_style + '\n    </namerecord>\n    <namerecord nameID="3" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      ' + font_creator + ' : ' + font_name + ' ' + font_style + ' : ' + font_creation_date + '\n    </namerecord>\n    <namerecord nameID="4" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      ' + font_name + ' ' + font_style + '\n    </namerecord>\n    <namerecord nameID="5" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      Version 001.001\n    </namerecord>\n    <namerecord nameID="6" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      ' + font_name + '-' + font_style + '\n    </namerecord>\n    <namerecord nameID="10" platformID="1" platEncID="0" langID="0x0" unicode="True">\n      Created by ' + font_creator + '\n    </namerecord>\n    <namerecord nameID="1" platformID="3" platEncID="1" langID="0x409">\n      ' + font_name + '\n    </namerecord>\n    <namerecord nameID="2" platformID="3" platEncID="1" langID="0x409">\n      ' + font_style + '\n    </namerecord>\n    <namerecord nameID="3" platformID="3" platEncID="1" langID="0x409">\n      ' + font_creator + ' : ' + font_name + ' ' + font_style + ' : ' + font_creation_date + '\n    </namerecord>\n    <namerecord nameID="4" platformID="3" platEncID="1" langID="0x409">\n      ' + font_name + ' ' + font_style + '\n    </namerecord>\n    <namerecord nameID="5" platformID="3" platEncID="1" langID="0x409">\n      Version 001.001\n    </namerecord>\n    <namerecord nameID="6" platformID="3" platEncID="1" langID="0x409">\n      ' + font_name + '-' + font_style + '\n    </namerecord>\n    <namerecord nameID="10" platformID="3" platEncID="1" langID="0x409">\n      Created by ' + font_creator + '\n    </namerecord>\n    <namerecord nameID="16" platformID="3" platEncID="1" langID="0x409">\n      ' + font_name + '\n    </namerecord>\n    <namerecord nameID="17" platformID="3" platEncID="1" langID="0x409">\n      ' + font_style + '\n    </namerecord>\n  </name>\n\n'

    # END OF NAME TABLE




    # START OF POST TABLE
    post_part_1 = '  <post>\n    <formatType value="2.0"/>\n    <italicAngle value="0.0"/>\n    <underlinePosition value="-125"/>\n    <underlineThickness value="50"/>\n    <isFixedPitch value="0"/>\n    <minMemType42 value="0"/>\n    <maxMemType42 value="0"/>\n    <minMemType1 value="0"/>\n    <maxMemType1 value="0"/>\n    <psNames>\n      <!-- This file uses unique glyph names based on the information\n           found in the "post" table. Since these names might not be unique,\n           we have to invent artificial names in case of clashes. In order to\n           be able to retain the original information, we need a name to\n           ps name mapping for those cases where they differ. Thats what\n           you see below.\n            -->\n    </psNames>\n    <extraNames>\n      <!-- following are the name that are not taken from the standard Mac glyph order -->\n      <psName name="CR"/>\n      <psName name="nbsp"/>\n    </extraNames>\n  </post>\n\n'
    # END OF POST TABLE




    # START OF GASP TABLE
    gasp_part_1 = '  <gasp>\n    <gaspRange rangeMaxPPEM="65535" rangeGaspBehavior="15"/>\n  </gasp>\n\n'
    # END OF GASP TABLE



    # START OF DSIG TABLE
    dsig_part_1 = '  <DSIG>\n    <!-- note that the Digital Signature will be invalid after recompilation! -->\n    <tableHeader flag="0x0" numSigs="0" version="1"/>\n  </DSIG>\n\n'
    # END OF DSIG TABLE


    closing_part_1 = '</ttFont>'


    # ALL UPDATING PART GOES HERE

    head_part_2 = '<xMin value="' + str(global_xmin) + '"/>\n    <yMin value="' + str(global_ymin) + '"/>\n    <xMax value="' + str(global_xmax) + '"/>\n    <yMax value="' + str(global_ymax) + '"/>'


    hhea_part_2 = '<ascent value="' + str(global_ymax) + '"/>\n    <descent value="' + str(global_ymin) + '"/>\n    <lineGap value="90"/>\n    <advanceWidthMax value="' + str(global_advance_width_max) + '"/>\n    <minLeftSideBearing value="0"/>\n    <minRightSideBearing value="0"/>\n    <xMaxExtent value="' + str(global_xmax) + '"/>'


    maxp_part_2 = '<maxPoints value="' + str(global_max_points) + '"/>\n    <maxContours value="' + str(global_max_contours) + '"/>'


    os_2_part_2 = '<xAvgCharWidth value="' + str(global_xavg_char_width) + '"/>'


    os_2_part_4 = '<usWinAscent value="' + str(global_ymax) + '"/>\n    <usWinDescent value="' + str(global_ymin) + '"/>\n    <ulCodePageRange1 value="00000000 00000000 00000000 00000001"/>\n    <ulCodePageRange2 value="00000000 00000000 00000000 00000000"/>\n    <sxHeight value="' + str(global_sx_height) + '"/>\n    <sCapHeight value="' + str(global_scap_height) + '"/>\n    <usDefaultChar value="0"/>\n    <usBreakChar value="32"/>\n    <usMaxContext value="1"/>\n  </OS_2>\n\n'


    string = starting_part_1 + glyphorder_part_1 + glyphorder_part_2 + glyphorder_part_3 + head_part_1 + head_part_2 + head_part_3 + hhea_part_1 + hhea_part_2 + hhea_part_3 + maxp_part_1 + maxp_part_2 + maxp_part_3 + os_2_part_1 + os_2_part_2 + os_2_part_3 + os_2_part_4 + hmtx_part_1 + hmtx_part_2 + hmtx_part_3 + cmap_part_1 + cmap_part_2 + cmap_part_3 + cmap_part_4 + cmap_part_5 + cmap_part_6 + cmap_part_7 + prep_part_1 + cvt_part_1 + loca_part_1 + glyf_part_1 + glyf_part_2 + name_part_1 + post_part_1 + gasp_part_1 + dsig_part_1 + closing_part_1

    ttx_file.write(string)

    ttx_file.close()
    
    return lowercase, uppercase, numbers, symbols
