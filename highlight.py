# -*- coding: utf8 -*-
import sublime
import sublime_plugin

DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_INVALID_COLOR = 'invalid'
DEFAULT_KEYWORD_COLOR = 'comment'

class HighlightText(sublime_plugin.EventListener):
    # example: todoTODO
    # example: 　
    def __init__(self):
        self.default_max_file_size = DEFAULT_MAX_FILE_SIZE
        self.delay = 0

    def is_too_bigview(self, view):
        max_size = self.default_max_file_size
        if max_size not in (None, False):
            max_size = int(max_size)
            current_size = view.size()
            if current_size > max_size:
                return True
        return False

    def highlight(self, view):
        settings = sublime.load_settings('Sublime-highlight.sublime-settings')
        invalid_pattern = settings.get('invalid')
        keyword_pattern = settings.get('keyword')

        if not view.window():
            return

        if self.is_too_bigview(view):
            self.clear_highlight(view)
            return

        if self.delay:
            sublime.set_timeout(self.update(view), self.delay)
        else:
            self.update(view)

        if invalid_pattern:
            view.add_regions('Highlight_invalid',
                view.find_all(invalid_pattern),
                DEFAULT_INVALID_COLOR,
                'dot',
                sublime.DRAW_EMPTY_AS_OVERWRITE |
                sublime.HIDE_ON_MINIMAP)

        if keyword_pattern:
            view.add_regions('Highlight_keyword',
                view.find_all(keyword_pattern),
                DEFAULT_KEYWORD_COLOR,
                'bookmark',
                sublime.DRAW_EMPTY_AS_OVERWRITE |
                sublime.HIDE_ON_MINIMAP)

    def clear_highlight(self, view):
        view.erase_regions('Highlight_invalid')
        view.erase_regions('Highlight_keyword')

    def update(self, view):
        pass

    def on_modified(self, view):
        self.highlight(view)

    def on_activated(self, view):
        self.highlight(view)

    def on_load(self, view):
        self.highlight(view)
