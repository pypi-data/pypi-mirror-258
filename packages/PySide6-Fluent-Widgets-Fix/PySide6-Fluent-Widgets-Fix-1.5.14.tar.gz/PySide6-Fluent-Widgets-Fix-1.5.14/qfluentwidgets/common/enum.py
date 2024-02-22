from PySide6.QtCore import Qt, QEvent, QPropertyAnimation, QFile, QEasingCurve
from PySide6.QtGui import QPainter, QPalette, QIcon, QKeySequence
from PySide6.QtWidgets import QStyle


# Fix memory leak
class QtEnum:
    class Qt:
        NoPen = Qt.NoPen
        white = Qt.white
        black = Qt.black
        transparent = Qt.transparent
        AlignCenter = Qt.AlignCenter
        ForegroundRole = Qt.ForegroundRole
        CheckStateRole = Qt.CheckStateRole
        DisplayRole = Qt.DisplayRole
        FontRole = Qt.FontRole
        DecorationRole = Qt.DecorationRole
        UserRole = Qt.UserRole
        AlignLeft = Qt.AlignLeft
        AlignRight = Qt.AlignRight
        AlignVCenter = Qt.AlignVCenter
        LeftButton = Qt.LeftButton
        NoItemFlags = Qt.NoItemFlags
    class QEasingCurve:
        OutQuad = QEasingCurve.OutQuad
    class QStyle:
        State_Enabled = QStyle.State_Enabled
        State_MouseOver = QStyle.State_MouseOver
    class QKeySequence:
        NativeText = QKeySequence.NativeText
    class QIcon:
        Disabled = QIcon.Disabled
        Selected = QIcon.Selected
        Normal = QIcon.Normal

    class QFile:
        ReadOnly = QFile.ReadOnly

    class QPalette:
        Text = QPalette.Text
        HighlightedText = QPalette.HighlightedText

    class QPropertyAnimation:
        Running = QPropertyAnimation.Running
        class State:
            Running = QPropertyAnimation.State.Running
            Stopped = QPropertyAnimation.State.Stopped

    class QPainter:
        Antialiasing = QPainter.Antialiasing
        TextAntialiasing = QPainter.TextAntialiasing
        SmoothPixmapTransform = QPainter.SmoothPixmapTransform

    class QFile:
        ReadOnly = QFile.ReadOnly

    class QEvent:
        WindowStateChange = QEvent.WindowStateChange
        Resize = QEvent.Resize
        MouseButtonPress = QEvent.MouseButtonPress
        MouseButtonRelease = QEvent.MouseButtonRelease
        Enter = QEvent.Enter
        Leave = QEvent.Leave
        Wheel = QEvent.Wheel
        Show = QEvent.Show

        class Type:
            EnabledChange = QEvent.Type.EnabledChange
            Enter = QEvent.Type.Enter
            Leave = QEvent.Type.Leave
            MouseButtonPress = QEvent.Type.MouseButtonPress
