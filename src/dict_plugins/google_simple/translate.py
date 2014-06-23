#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou Shaohui, Wang Yong
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
#             Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import pyqtSlot
from auto_object import AutoQObject
from translate_window import TranslateWindow
import requests
from config import setting_config
import os
from deepin_utils.file import get_parent_dir
from utils import safe_eval
from nls import _
from tts_interface import get_voice_simple, get_phonetic_symbol
            
class Translate(TranslateWindow):
    
    def __init__(self):
        TranslateWindow.__init__(self, os.path.join(get_parent_dir(__file__), "Translate.qml"))
        

    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("text", str),
            ("translate", str),
            ("phonetic", str),
            ("voices", 'QVariant'),
            ("fixed", str),
          name="TranslateInfo")
        self.translate_info = TranslateInfo()        
        
    def parse_dummy_list(self, dlist):
        while ",," in dlist or "[," in dlist:
            dlist = dlist.replace(",,", ",None,").replace("[,", "[None,")
        try:    
            return safe_eval(dlist)
        except SyntaxError:
            return []
        
    def get_word_translate(self, glist):
        
        def parse_list(word_list):
            try:
                title = word_list[0]
                content = "; ".join(word_list[1])
                return "%s:  %s" % (title, content)
            except:
                return None
        
        try:
            noun_list = glist[1][0]
        except:    
            noun = None
        else:    
            noun = parse_list(noun_list)
            
        try:    
            verb_list = glist[1][1]
        except:
            verb = None
        else:    
            verb = parse_list(verb_list)
            
        if not noun and not verb:
            return self.get_sample_result(glist)
        
        ret = []
        if noun is not None:
            ret.append(noun)
        if verb is not None:    
            ret.append(verb)
        return "\n".join(ret)    
     
    def get_sample_result(self, glist):
        try:
            return  ''.join([dl[0] for dl in glist[0]])
        except:
            return _("Translate failed")
    
    def google_translate(self, text, sl="auto", tl="en", encoding="UTF-8"):
        target_language = tl
        source_language = sl
        input_encoding = output_encoding = encoding
        data = dict(client="t",
                    hl=tl,
                    sl=source_language,
                    tl=target_language,
                    ie=input_encoding,
                    oe=output_encoding,
                    otf=1,
                    ssel=0,
                    pc=1,
                    uptl=target_language,
                    sc=2,
                    q=text)    
        url = "http://translate.google.cn/translate_a/t"
        dummy_list = requests.get(url, params=data).text
        plist = self.parse_dummy_list(dummy_list)
        result = self.get_word_translate(plist)
        return result.decode(encoding).strip()
        
    @pyqtSlot(str)
    def get_translate(self, text):
        self.translate_info.text = text
        self.translate_info.voices = get_voice_simple(text)
        self.translate_info.phonetic = get_phonetic_symbol(text)
        self.translate_info.translate = self.google_translate(
            text,
            tl=setting_config.get_translate_config("dst_lang"),
            )

    @pyqtSlot()    
    def clear_translate(self):
        self.translate_info.text = ""
        self.translate_info.translate = ""
        self.translate_info.voice = None
        self.translate_info.phonetic = ""
