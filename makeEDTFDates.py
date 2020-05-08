#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# makeEDTFDates

import csv
import logging
import re
import shutil
import sys
from tempfile import NamedTemporaryFile
from edtf import text_to_edtf

FILES = [
    "letters"
]
ONLYADD = False
DRY_RUN = False

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger()


def prepareDate(datestring):
    replacements = [
        ('[', ''),
        (']', ''),
        (' vor oder am ', ' vor ')
    ]
    for repl in replacements:
        datestring = datestring.replace(repl[0], repl[1])

    # normalize whitespace
    datestring = re.sub(r'\s{2,}', ' ', datestring)

    # EDTF parser doesn't understand start, mid or end of a month
    # Default:  1540 März Ende  > 1540-03
    # Wanted:                   > 1540-03-21/1540-03-31

    # 1547/48   >   1547/1548
    def completeSecondYear(mo):
        return mo.group(1) + mo.group(2) + mo.group(1) + mo.group(3)
    datestring = re.sub(r'(\d\d)(\d\d/)(\d\d)', completeSecondYear, datestring)

    # 1535 [=1534] Dezember 25  >  1534 Dezember 25
    if '=' in datestring:
        datestring = datestring.split('=')[-1]

    return datestring


def postprocessDate(datestring, edtf):
    if edtf:
        # Update EDTF to current draft
        # https://www.loc.gov/standards/datetime/edtf.html
        # 'unknown' is replaced by ''
        edtf = re.sub(r'unknown', '', edtf)
        # 'open' is replaced by ''
        edtf = re.sub(r'open', '..', edtf)
        # certainty
        if '?' in datestring and '?' not in edtf:
            # add questionmark if found in datestring and still not in edtf
            edtf = edtf + '?'
        # all of a set, needs to be converted to one of a set, because it's not
        # yet supported by csv2cmi.
        # {xxxx,xxxx,xxxx} > [xxxx,xxxx,xxxx]
        edtf = re.sub(r'{', '[', edtf)
        edtf = re.sub(r'}', ']', edtf)
        # translate seasons (except winter) to interval, because it's not yet supported by
        # csv2cmi.
        # spring: DDDD-21 > DDDD-03-01/DDDD-05-31
        # summer: DDDD-22 > DDDD-06-01/DDDD-08-31
        # autumn: DDDD-23 > DDDD-09-01/DDDD-11-30
        edtf = re.sub(r'(\d{4})-21', r'\1-03-01/\1-05-31', edtf)
        edtf = re.sub(r'(\d{4})-22', r'\1-06-01/\1-08-31', edtf)
        edtf = re.sub(r'(\d{4})-23', r'\1-09-01/\1-11-30', edtf)
    return edtf


def prepareDateSets(datestring):
    if ' or ' in datestring or ' and ' in datestring or '/' in datestring or (('-' in datestring or ' to ' in datestring) and not re.search(r'\d{4}\-\d{4}', datestring)) or ('after ' in datestring and 'before ' in datestring and '/' in datestring):
        # cleanup
        datestring = datestring.replace('between ', '')
        datestring = datestring.replace('after ', '')
        datestring = datestring.replace('before ', '')
        # complete date sets, so that each single date could be parsed
        matches = []
        pattern = r'(\d{4}\s?)?([A-Z]\w+\s?)?(beginning\s|middle\s|end\s|\d{1,2})?'
        for match in re.findall(pattern, datestring):
            if match != ('', '', ''):
                matches.append(list(map(str.strip, match)))
        # simple alternative
        if len(matches) == 2:
            # add year of first to second
            if matches[0][0] and not matches[1][0]:
                matches[1][0] = matches[0][0]
                # also add month, if not given
                if matches[0][1] and not matches[1][1]:
                    matches[1][1] = matches[0][1]
            # Remove empties
            fm = list(filter(None, matches[0]))
            to = list(filter(None, matches[1]))
            return (' '.join(fm), ' '.join(to))
        return datestring.split(' or ')
    return datestring


def simpleTranslate(text):
    de_en = [
        ('Januar', 'January'),
        ('Februar', 'February'),
        ('März', 'March'),
        ('Mai', 'May'),
        ('Juni', 'June'),
        ('Juli', 'July'),
        ('Oktober', 'October'),
        ('Dezember', 'December'),
        ('vor', 'before'),
        ('nach', 'after'),
        ('kurz', 'shortly'),
        ('etwa', 'about'),
        ('um', 'around'),
        ('nicht', 'not'),
        ('Anfang', 'beginning'),
        ('Ende', 'end'),
        ('Mitte', 'middle'),
        ('zwischen', 'between'),
        ('und', 'and'),
        ('oder', 'or'),
        ('von', 'from'),
        ('bis', 'to'),
        ('Frühling', 'spring'),
        ('Frühjahr', 'spring'),
        ('Sommer', 'summer'),
        ('Herbst', 'autumn'),
        ('Winter', 'winter'),
        ('bald', 'soon'),
        ('früher als', 'earlier than'),
        ('später als', 'later than')
    ]
    for trans in de_en:
        text = text.replace(trans[0], trans[1])
    return text


def getEDTF(datetext, letter_key=None):
    ''' datetext is a German. It needs be translated to English to be parsable
    by the edtf library afterwards.
    '''
    try:
        translated = simpleTranslate(prepareDate(datetext))
        prepared_translated = prepareDateSets(translated)
        if not isinstance(prepared_translated, str):
            try:
                if ' between ' in translated or ('-' in translated or ' to ' in translated) and not re.search(r'\d{4}\-\d{4}',translated) or ('after ' in translated and 'before ' in translated and '/' in translated):
                    edtf = '/'.join(map(text_to_edtf, prepared_translated))
                elif ' and ' in translated:
                    edtf = '{' + ','.join(map(text_to_edtf, prepared_translated)) + '}'
                else:
                    edtf = '[' + ','.join(map(text_to_edtf, prepared_translated)) + ']'
            except Exception as e:
                raise e
                edtf = None
        else:
            try:
                edtf = text_to_edtf(prepared_translated)
            except Exception as e:
                raise e
                edtf = None
    except Exception as e:
        raise e

    # run postprocessing of date
    edtf = postprocessDate(translated, edtf)
    log.debug(datetext)
    log.debug((letter_key, edtf))
    return edtf


for input_filename in FILES:
    filename = input_filename + '.csv'
    tempfile = NamedTemporaryFile(mode='w+t', delete=False)
    if DRY_RUN:
        log.info('Dry run. Output will be written to temporary file {}'
                 .format(tempfile.name))
    if ONLYADD:
        log.info('Dates are added to empty cells only.')

    with open(filename, 'r') as csvfile, tempfile:
        dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        dictwriter = csv.DictWriter(tempfile,
                                    fieldnames=dictreader.fieldnames,
                                    delimiter=',',
                                    quoting=csv.QUOTE_ALL)
        dictwriter.writeheader()
        for row in dictreader:
            for type in ('senderDate', 'addresseeDate'):
                if type + 'Text' in row and type in row and row[type + 'Text'] and (not row[type] or not ONLYADD):
                    edtf = getEDTF(
                        row[type + 'Text'],
                        row['key'])
                    row[type] = edtf
                    log.info('Added "{}" to {} at line {} parsed from "{}"'
                             .format(edtf,
                                     type,
                                     dictreader.line_num,
                                     row[type + 'Text']))
            dictwriter.writerow(row)

    if not DRY_RUN:
        shutil.move(tempfile.name, filename)
