#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.19 02:00:00                  #
# ================================================== #

from pygpt_net.core.dispatcher import Event
from pygpt_net.item.ctx import CtxItem


class Audio:
    def __init__(self, window=None):
        """
        Audio/voice controller

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup controller"""
        self.update()

    def toggle_input(self, state: bool, btn: bool = True):
        """
        Toggle audio input

        :param state: True to enable, False to disable
        :param btn: True if called from button
        """
        self.window.core.dispatcher.dispatch(
            Event(Event.AUDIO_INPUT_TOGGLE, {
                "value": state,
            })
        )

    def toggle_output(self):
        """Toggle audio output"""
        if self.window.controller.plugins.is_enabled('audio_azure'):
            self.disable_output()
        else:
            self.enable_output()

    def enable_output(self):
        """Enable audio output"""
        self.window.controller.plugins.enable('audio_azure')
        if self.window.controller.plugins.is_enabled('audio_azure') \
                and (self.window.core.plugins.plugins['audio_azure'].options['azure_api_key'] is None
                     or self.window.core.plugins.plugins['audio_azure'].options['azure_api_key'] == ''):
            self.window.ui.dialogs.alert("Azure API KEY is not set. Please set it in plugins settings.")
            self.window.controller.plugins.disable('audio_azure')
        self.window.core.config.save()
        self.update()

    def disable_output(self):
        """Disable audio output"""
        self.window.controller.plugins.disable('audio_azure')
        self.window.core.config.save()
        self.update()

    def disable_input(self, update: bool = True):
        """
        Disable audio input

        :param update: True to update menu and listeners
        """
        self.window.controller.plugins.disable('audio_openai_whisper')
        self.window.core.config.save()
        if update:
            self.update()

    def stop_input(self):
        """Stop audio input"""
        self.window.core.dispatcher.dispatch(
            Event(Event.AUDIO_INPUT_STOP, {
                "value": True,
            }), all=True)

    def stop_output(self):
        """Stop audio output"""
        self.window.core.dispatcher.dispatch(
            Event(Event.AUDIO_OUTPUT_STOP, {
                "value": True,
            }), all=True)

    def update(self):
        """Update UI and listeners"""
        self.update_listeners()
        self.update_menu()

    def is_output_enabled(self) -> bool:
        """
        Check if any audio output is enabled

        :return: True if enabled
        """
        if self.window.controller.plugins.is_enabled('audio_azure') \
                or self.window.controller.plugins.is_enabled('audio_openai_tts'):
            return True
        return False

    def update_listeners(self):
        """Update audio listeners"""
        is_output = False
        if self.window.controller.plugins.is_enabled('audio_azure'):
            is_output = True
        if self.window.controller.plugins.is_enabled('audio_openai_tts'):
            is_output = True
        if not is_output:
            self.stop_output()

        if not self.window.controller.plugins.is_enabled('audio_openai_whisper'):
            self.toggle_input(False)
            self.stop_input()
            if self.window.ui.plugin_addon['audio.input'].btn_toggle.isChecked():
                self.window.ui.plugin_addon['audio.input'].btn_toggle.setChecked(False)

    def update_menu(self):
        """Update audio menu"""
        if self.window.controller.plugins.is_enabled('audio_azure'):
            self.window.ui.menu['audio.output.azure'].setChecked(True)
        else:
            self.window.ui.menu['audio.output.azure'].setChecked(False)

        if self.window.controller.plugins.is_enabled('audio_openai_tts'):
            self.window.ui.menu['audio.output.tts'].setChecked(True)
        else:
            self.window.ui.menu['audio.output.tts'].setChecked(False)

        if self.window.controller.plugins.is_enabled('audio_openai_whisper'):
            self.window.ui.menu['audio.input.whisper'].setChecked(True)
        else:
            self.window.ui.menu['audio.input.whisper'].setChecked(False)

    def read_text(self, text: str):
        """
        Read text using audio output plugins

        :param text: text to read
        """
        ctx = CtxItem()
        ctx.output = text
        all = False
        if self.window.controller.audio.is_output_enabled():
            event = Event(Event.CTX_AFTER)
        else:
            all = True  # to all plugins (even if disabled)
            event = Event(Event.AUDIO_READ_TEXT)
        event.ctx = ctx
        self.window.core.dispatcher.dispatch(event, all=all)
