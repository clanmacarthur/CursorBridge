Attribute VB_Name = "CleanDates"
Option Explicit

Public Sub CleanDates_Col5_AllSheets()
    Dim ws As Worksheet
    For Each ws In ThisWorkbook.Worksheets
        CleanDates_OnSheet ws, 5
    Next ws
End Sub

Public Sub CleanDates_Col5_ActiveSheet()
    CleanDates_OnSheet ActiveSheet, 5
End Sub

Private Sub CleanDates_OnSheet(ByVal ws As Worksheet, ByVal targetCol As Long)
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, targetCol).End(xlUp).Row

    Dim re As Object
    Set re = CreateObject("VBScript.RegExp")
    re.Pattern = "\b(\d{1,2})(st|nd|rd|th)(,?)"
    re.Global = True
    re.IgnoreCase = True

    Dim r As Long
    For r = 1 To lastRow
        Dim v As Variant: v = ws.Cells(r, targetCol).Value
        If VarType(v) = vbString Then
            Dim s As String: s = CStr(v)
            Dim newVal As String: newVal = re.Replace(s, "$1,")
            If newVal <> s Then ws.Cells(r, targetCol).Value = newVal
        End If
    Next r
End Sub


