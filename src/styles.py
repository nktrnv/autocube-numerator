WINDOW_STYLES = {
    "bg": "#FFFFFF",
}

LABEL_STYLES = {
    **WINDOW_STYLES,
    "font": ("Arial", 11),
    "bd": 0,
}

BUTTON_STYLES = {
    **LABEL_STYLES,
    "height": 2,
    "bg": "#F2F2F2",
    "fg": "#000000",
    "activeforeground": "#000000",
    "activebackground": "#E5E5E5",
}

PRIMARY_BUTTON_STYLES = {
    **BUTTON_STYLES,
    "bg": "#E84850",
    "fg": "#FFFFFF",
    "activeforeground": "#FFFFFF",
    "activebackground": "#D81B24",
}

ENTRY_STYLES = {
    **LABEL_STYLES,
    "bg": "#F2F2F2",
}
