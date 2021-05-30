import win32clipboard


def to_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


def get_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data
