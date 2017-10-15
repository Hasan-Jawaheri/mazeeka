# -*- coding: utf-8 -*-

import glob, sys, time, os
import mutagen
from mutagen.mp4 import MP4, MP4Cover

arabic_alphabet = u'غظضذخثتشرقصفعسنملكيطحزوهدجباأطةإلهى'
bad_words = ['غنية', 'بالكلمات', 'اجمل', 'اغاني', 'غلطة', 'الشاطر', 'ب', 'لف', 'و', 'السيدة', '(فيديو كليب)', '', 'القيصر', 'للقيصر', 'فيديو', 'كليب', 'ملكة', 'جمال', 'العرب', 'كلوديا', 'حنا', 'حفلة', 'جرش', 'ليلة عمر', 'اغنيه', 'النسخه الاصليه', 'الرماس ميوزك']
g_artists = ['الين لحود', 'كارول صقر', 'عاصي حلاني', 'عمرو دياب', 'عاصي الحلاني', 'ملحم زين', 'دينا حايك', 'مروان خورى', 'ليسا', 'سميرة سعيد', 'وا ل كفورى', 'عاصى الحلانى', 'صابر الرباعي', 'سعد لمجرد', 'راغب علامة', 'وا ل كفوري', 'يارا', 'فضل شاكر', 'نوال الزغبى', 'فيروز', 'راغب علامة' 'عاصى الحلانى', 'ماجد المهندس', 'جميلة', 'ديانا حداد', 'وائل كفوري', 'مروان خوري', 'راشد الماجد', 'نجوى كرم', 'نوال الزغبي', 'حسين الجسمي', 'شيرين', 'كارول سماحة', 'نانسي عجرم', ' صابر الرباعي', 'كاظم الساهر', 'اليسا', 'راغب علامه', 'نانسي عجرم', 'كاظم الساهر', 'الهام المدفعي', 'إلهام المدفعي', 'حاتم العراقي', 'حازم جابر', 'احمد المصلاوي', 'احمد شاكر', 'اوراس ستار', 'جعفر الغزال', 'محمد حالف', 'حسين الطيب', 'حسين الغزال', 'صلاح حسن', 'نصرت البدر', 'نور الزين', 'وليد الشامي', 'ماجد المهندس', 'محمود الشاعري', 'نصر البحار', ]
g_artists_map = {
    'ليسا': 'اليسا',
    'مروان خورى': 'مروان خوري',
    'عاصي حلاني': 'عاصي الحلاني',
}

def remove_nonarabic(text):
    text = map(lambda x: x if x in arabic_alphabet else ' ', list(text))
    return "".join(text)

def remove_extra_spaces(text):
    i = 0
    while i < len(text)-1:
        if (text[i] == ' ' and text[i+1] == ' '):
            text = text[:i] + text[i+1:]
        else:
            i += 1
    return text.strip()

def remove_bad_words(text):
    words = text.split(' ')
    output = ''
    for w in words:
        if w not in bad_words:
            output += w + ' '
    if len(output) > 0 and (output[-1] == ' '):
        output = output[:len(output)-1]
    return output

def parse_name(text):
    artists = []
    for artist in g_artists:
        if artist in text:
            artists += [artist]
            text = remove_extra_spaces(text.replace(artist, ' '))
    F = lambda x: "".join(x)
    return (list(map(F, artists)), F(text))

def parse_song_title(title):
    # returns ([artists], song title)
    (artists, song_title) = parse_name(remove_bad_words(remove_extra_spaces(remove_nonarabic(title))))
    for i in range(len(artists)):
        if artists[i] in g_artists_map:
            artists[i] = g_artists_map[artists[i]]
    if artists == []:
        artists = [""]
    if song_title == "":
        song_title = title
    return (artists, song_title)

def fix_audio_file(filename, song, artist, thumbnail):
    audio = MP4(filename)
    audio["\xa9nam"] = song
    audio["\xa9ART"] = artist

    if thumbnail:
        audio["covr"] = [MP4Cover(thumbnail, imageformat=MP4Cover.FORMAT_JPEG)]

    audio.save()