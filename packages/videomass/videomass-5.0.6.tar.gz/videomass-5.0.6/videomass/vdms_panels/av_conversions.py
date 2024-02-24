# -*- coding: UTF-8 -*-
"""
FileName: av_conversions.py
Porpose: audio/video conversions interface
Compatibility: Python3, wxPython4 Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyleft - 2024 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.13.2024
Code checker: flake8, pylint

This file is part of Videomass.

   Videomass is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Videomass is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Videomass.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import wx
import wx.lib.scrolledpanel as scrolled
import wx.lib.agw.floatspin as FS
from pubsub import pub
from videomass.vdms_utils.get_bmpfromsvg import get_bmp
from videomass.vdms_utils.utils import get_volume_data
from videomass.vdms_panels.libaom import AV1Pan
from videomass.vdms_panels.webm import WebMPan
from videomass.vdms_panels.hevc_avc import Hevc_Avc
from videomass.vdms_io.io_tools import volume_detect_process
from videomass.vdms_io.io_tools import stream_play
from videomass.vdms_io.checkup import check_files
from videomass.vdms_dialogs.epilogue import Formula
from videomass.vdms_dialogs import audiodialogs
from videomass.vdms_dialogs import presets_addnew
from videomass.vdms_dialogs.filter_crop import Crop
from videomass.vdms_dialogs.filter_transpose import Transpose
from videomass.vdms_dialogs.filter_denoisers import Denoisers
from videomass.vdms_dialogs.filter_deinterlace import Deinterlace
from videomass.vdms_dialogs.filter_scale import Scale
from videomass.vdms_dialogs.filter_stab import VidstabSet
from videomass.vdms_dialogs.filter_colorcorrection import ColorEQ
from videomass.vdms_dialogs.shownormlist import AudioVolNormal


class AV_Conv(wx.Panel):
    """
    Panel GUI for audio and video conversions
    """
    # colour rappresentetion in html
    AZURE = '#15a6a6'
    YELLOW = '#bd9f00'
    RED = '#ea312d'
    ORANGE = '#f28924'
    GREENOLIVE = '#6aaf23'
    GREEN = '#268826'
    CYAN = '#61ccc7'  # rgb form (wx.Colour(97, 204, 199)
    VIOLET = '#D64E93'
    LIMEGREEN = '#87A615'
    TROPGREEN = '#15A660'
    WHITE = '#fbf4f4'
    BLACK = '#060505'

    ASPECTRATIO = [("Auto"), ("1:1"), ("1.3333"), ("1.7777"), ("2.4:1"),
                   ("3:2"), ("4:3"), ("5:4"), ("8:7"), ("14:10"), ("16:9"),
                   ("16:10"), ("19:10"), ("21:9"), ("32:9"),
                   ]
    FPS = [("Auto"), ("ntsc"), ("pal"), ("film"), ("23.976"), ("24"),
           ("25"), ("29.97"), ("30"), ("48"), ("50"), ("59.94"), ("60"),
           ]
    PIXELFRMT = [('None'), ('gray'), ('gray10le'), ('nv12'), ('nv16'),
                 ('nv20le'), ('nv21'), ('yuv420p'), ('yuv420p10le'),
                 ('yuv422p'), ('yuv422p10le'), ('yuv444p'), ('yuv444p10le'),
                 ('yuvj420p'), ('yuvj422p'), ('yuvj444p'),
                 ]
    # MUXERS dictionary:
    MUXERS = {'mkv': 'matroska', 'avi': 'avi', 'mp4': 'mp4',
              'm4v': 'null', 'ogg': 'ogg', 'webm': 'webm',
              }
    # Namings in the video container selection combo box:
    VCODECS = ({"Mpeg4": {"-c:v mpeg4": ["avi"]},
                "H.264": {"-c:v libx264": ["mkv", "mp4", "avi", "m4v"]},
                "H.265": {"-c:v libx265": ["mkv", "mp4", "avi", "m4v"]},
                "AV1": {"-c:v libaom-av1": ["mkv", "webm", "mp4"]},
                "Theora": {"-c:v libtheora": ["ogv", "mkv"]},
                "Vp8": {"-c:v libvpx": ["webm"]},
                "Vp9": {"-c:v libvpx-vp9": ["webm", "mkv", "mp4"]},
                "Copy": {"-c:v copy": ["mkv", "mp4", "avi", "m4v",
                                       "ogv", "webm", "Copy"]}
                })
    # Namings in the audio codec selection on audio radio box:
    ACODECS = {('Auto'): (""),
               ('PCM'): ("pcm_s16le"),
               ('FLAC'): ("flac"),
               ('AAC'): ("aac"),
               ('ALAC'): ("alac"),
               ('AC3'): ("ac3"),
               ('VORBIS'): ("libvorbis"),
               ('LAME'): ("libmp3lame"),
               ('OPUS'): ("libopus"),
               ('Copy'): ("copy"),
               ('No Audio'): ("-an")
               }
    # Namings in the audio format selection on Container combobox:
    A_FORMATS = ('wav', 'mp3', 'ac3', 'ogg', 'flac', 'm4a', 'aac')
    # compatibility between video formats and related audio codecs:
    AV_FORMATS = {('avi'): ('default', 'wav', None, None, None, 'ac3', None,
                            'mp3', None, 'copy', 'mute'),
                  ('mp4'): ('default', None, None, 'aac', None, 'ac3', None,
                            'mp3', 'opus', 'copy', 'mute'),
                  ('m4v'): ('default', None, None, 'aac', 'alac', None, None,
                            None, None, 'copy', 'mute'),
                  ('mkv'): ('default', 'wav', 'flac', 'aac', None, 'ac3',
                            'ogg', 'mp3', 'opus', 'copy', 'mute'),
                  ('webm'): ('default', None, None, None, None, None, 'ogg',
                             None, 'opus', 'copy', 'mute'),
                  ('ogv'): ('default', None, 'flac', None, None, None, 'ogg',
                            None, 'opus', 'copy', 'mute'),
                  ('wav'): (None, 'wav', None, None, None, None, None, None,
                            None, 'copy', None),
                  ('mp3'): (None, None, None, None, None, None, None, 'mp3',
                            None, 'copy', None),
                  ('ac3'): (None, None, None, None, None, 'ac3', None, None,
                            None, 'copy', None),
                  ('ogg'): (None, None, None, None, None, None, 'ogg', None,
                            'opus', 'copy', None),
                  ('flac'): (None, None, 'flac', None, None, None, None, None,
                             None, 'copy', None),
                  ('m4a'): (None, None, None, None, 'alac', None, None, None,
                            None, 'copy', None),
                  ('aac'): (None, None, None, 'aac', None, None, None, None,
                            None, 'copy', None),
                  }
    # ------------------------------------------------------------------#

    def __init__(self, parent, appdata, icons):
        """
        Collects all the values of the
        GUI controls used in this panel
        """
        if 'wx.svg' in sys.modules:  # only available in wx version 4.1 to up
            bmpplay = get_bmp(icons['preview'], ((16, 16)))
            bmpapreview = get_bmp(icons['preview_audio'], ((16, 16)))
            self.bmpreset = get_bmp(icons['clear'], ((16, 16)))
            bmpresize = get_bmp(icons['scale'], ((16, 16)))
            bmpcrop = get_bmp(icons['crop'], ((16, 16)))
            bmprotate = get_bmp(icons['rotate'], ((16, 16)))
            bmpdeinterlace = get_bmp(icons['deinterlace'], ((16, 16)))
            bmpdenoiser = get_bmp(icons['denoiser'], ((16, 16)))
            bmpanalyzes = get_bmp(icons['volanalyze'], ((16, 16)))
            bmpasettings = get_bmp(icons['settings'], ((16, 16)))
            bmppeaklevel = get_bmp(icons['audiovolume'], ((16, 16)))
            bmpstab = get_bmp(icons['stabilizer'], ((16, 16)))
            bmpsaveprf = get_bmp(icons['addtoprst'], ((16, 16)))
            bmpcoloreq = get_bmp(icons['coloreq'], ((16, 16)))
        else:
            bmpplay = wx.Bitmap(icons['preview'], wx.BITMAP_TYPE_ANY)
            bmpapreview = wx.Bitmap(icons['preview_audio'], wx.BITMAP_TYPE_ANY)
            self.bmpreset = wx.Bitmap(icons['clear'], wx.BITMAP_TYPE_ANY)
            bmpresize = wx.Bitmap(icons['scale'], wx.BITMAP_TYPE_ANY)
            bmpcrop = wx.Bitmap(icons['crop'], wx.BITMAP_TYPE_ANY)
            bmprotate = wx.Bitmap(icons['rotate'], wx.BITMAP_TYPE_ANY)
            bmpdeinterlace = wx.Bitmap(icons['deinterlace'],
                                       wx.BITMAP_TYPE_ANY)
            bmpdenoiser = wx.Bitmap(icons['denoiser'], wx.BITMAP_TYPE_ANY)
            bmpanalyzes = wx.Bitmap(icons['volanalyze'], wx.BITMAP_TYPE_ANY)
            bmpasettings = wx.Bitmap(icons['settings'], wx.BITMAP_TYPE_ANY)
            bmppeaklevel = wx.Bitmap(icons['audiovolume'], wx.BITMAP_TYPE_ANY)
            bmpstab = wx.Bitmap(icons['stabilizer'], wx.BITMAP_TYPE_ANY)
            bmpsaveprf = wx.Bitmap(icons['addtoprst'], wx.BITMAP_TYPE_ANY)
            bmpcoloreq = wx.Bitmap(icons['coloreq'], wx.BITMAP_TYPE_ANY)

        # Args settings definition
        self.opt = {
            "VidCmbxStr": "x264", "OutputFormat": "mkv",
            "VideoCodec": "-c:v libx264", "ext_input": "",
            "Passing": "1 pass", "InputDir": "", "OutputDir": "",
            "VideoSize": "", "AspectRatio": "", "FPS": "", "Preset": "",
            "Profile": "", "Level": "", "Tune": "", "VideoBitrate": "",
            "CRF": "", "WebOptim": "",
            "MinRate": "", "MaxRate": "", "Bufsize": "", "AudioCodStr": "",
            "AudioIndex": "", "AudioMap": ["-map 0:a:?", ""],
            "SubtitleMap": "-map 0:s?", "AudioCodec": ["", ""],
            "AudioChannel": ["", ""], "AudioRate": ["", ""],
            "AudioBitrate": ["", ""], "AudioDepth": ["", ""], "PEAK": [],
            "EBU": "", "RMS": [], "Deinterlace": "", "Interlace": "",
            "PixelFormat": "", "Orientation": ["", ""], "Crop": "",
            "CropColor": "", "Scale": "", "Setdar": "", "Setsar": "",
            "Denoiser": "", "Vidstabtransform": "", "Vidstabdetect": "",
            "Unsharp": "", "Makeduo": False, "VFilters": "",
            "PixFmt": "-pix_fmt yuv420p", "Deadline": "", "CpuUsed": "",
            "RowMthreading": "", "Usage": "", "GOP": "", "ColorEQ": "",
        }
        self.appdata = appdata
        self.parent = parent

        if self.appdata['ostype'] == 'Windows':
            sizepancodevideo = (270, 700)
        elif self.appdata['ostype'] == 'Darwin':
            sizepancodevideo = (300, 700)
        else:
            if int(''.join(wx.version().split()[0].split('.'))) >= 410:
                sizepancodevideo = (300, 700)
            else:
                sizepancodevideo = (350, 700)

        wx.Panel.__init__(self, parent, -1)
        # ------------ widgets
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        # ------------------ BEGIN BOX top
        sizer_base.Add(10, 10)
        sizer_convin = wx.BoxSizer(wx.HORIZONTAL)
        txtmedia = wx.StaticText(self, wx.ID_ANY, _('Media:'))
        sizer_convin.Add(txtmedia, 0, wx.LEFT | wx.CENTRE, 5)
        self.cmb_Media = wx.ComboBox(self, wx.ID_ANY,
                                     choices=['Video', 'Audio'],
                                     size=(100, -1), style=wx.CB_DROPDOWN
                                     | wx.CB_READONLY
                                     )
        sizer_convin.Add(self.cmb_Media, 0, wx.LEFT | wx.CENTRE, 5)
        txtFormat = wx.StaticText(self, wx.ID_ANY, _('Container:'))
        sizer_convin.Add(txtFormat, 0, wx.LEFT | wx.CENTRE, 20)
        choices = list(AV_Conv.VCODECS['H.264'].values())[0]
        self.cmb_Vcont = wx.ComboBox(self, wx.ID_ANY,
                                     choices=choices,
                                     size=(100, -1),
                                     style=wx.CB_DROPDOWN
                                     | wx.CB_READONLY,
                                     )
        sizer_convin.Add(self.cmb_Vcont, 0, wx.LEFT | wx.CENTRE, 5)
        self.ckbx_web = wx.CheckBox(self, wx.ID_ANY, (_('Use for Web')))
        sizer_convin.Add(self.ckbx_web, 0, wx.LEFT | wx.CENTRE, 20)
        self.btn_saveprst = wx.Button(self, wx.ID_ANY,
                                      _("Save Preset"), size=(-1, -1))
        self.btn_saveprst.SetBitmap(bmpsaveprf, wx.LEFT)
        sizer_convin.Add(self.btn_saveprst, 0, wx.LEFT | wx.CENTRE, 20)
        msg = _("Target")
        box1 = wx.StaticBox(self, wx.ID_ANY, msg)
        box_convin = wx.StaticBoxSizer(box1, wx.HORIZONTAL)
        box_convin.Add(sizer_convin, 0, wx.ALL | wx.CENTRE, 5)
        sizer_base.Add(box_convin, 0, wx.BOTTOM | wx.CENTRE, 5)
        # END BOX top Media and Format

        # ------------------ BEGIN NOTEBOOK CONSTRUCTOR
        self.notebook = wx.Notebook(self, wx.ID_ANY,
                                    style=wx.NB_NOPAGETHEME | wx.NB_TOP
                                    )
        sizer_base.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)

        # -------------- BEGIN NOTEBOOK PANEL 1
        self.nb_Video = wx.Panel(self.notebook, wx.ID_ANY)
        sizer_nbVideo = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.StaticBox(self.nb_Video, wx.ID_ANY, _("Video Encoder"))
        self.box_Vcod = wx.StaticBoxSizer(box2, wx.VERTICAL)
        sizer_nbVideo.Add(self.box_Vcod, 0, wx.ALL | wx.EXPAND, 5)
        self.codVpanel = scrolled.ScrolledPanel(self.nb_Video, -1,
                                                size=sizepancodevideo,
                                                style=wx.TAB_TRAVERSAL
                                                | wx.BORDER_NONE,
                                                name="panelscroll",
                                                )
        self.box_Vcod.Add(self.codVpanel, 0, wx.CENTER)
        grid_sx_Vcod = wx.FlexGridSizer(11, 2, 0, 0)
        txtVcod = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Encoder')
        grid_sx_Vcod.Add(txtVcod, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_Vcod = wx.ComboBox(self.codVpanel, wx.ID_ANY,
                                    choices=list(AV_Conv.VCODECS.keys()),
                                    size=(120, -1),
                                    style=wx.CB_DROPDOWN | wx.CB_READONLY
                                    )
        grid_sx_Vcod.Add(self.cmb_Vcod, 0, wx.ALL, 5)
        txtpass = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Passes')
        grid_sx_Vcod.Add(txtpass, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.ckbx_pass = wx.CheckBox(self.codVpanel, wx.ID_ANY, "Two-pass")
        grid_sx_Vcod.Add(self.ckbx_pass, 0, wx.ALL, 5)
        txtCRF = wx.StaticText(self.codVpanel, wx.ID_ANY, 'CRF')
        grid_sx_Vcod.Add(txtCRF, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.slider_CRF = wx.Slider(self.codVpanel, wx.ID_ANY, 1, -1, 51,
                                    size=(150, -1), style=wx.SL_HORIZONTAL
                                    | wx.SL_AUTOTICKS
                                    | wx.SL_LABELS,
                                    )
        grid_sx_Vcod.Add(self.slider_CRF, 0, wx.ALL, 5)
        txtVbrate = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Bit Rate (kb)')
        grid_sx_Vcod.Add(txtVbrate, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.spin_Vbrate = wx.SpinCtrl(self.codVpanel, wx.ID_ANY,
                                       "-1", min=-1, max=204800,
                                       style=wx.TE_PROCESS_ENTER
                                       )
        grid_sx_Vcod.Add(self.spin_Vbrate, 0, wx.ALL, 5)
        txtMinr = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Min Rate (kb)')
        grid_sx_Vcod.Add(txtMinr, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.spinMinr = wx.SpinCtrl(self.codVpanel, wx.ID_ANY,
                                    "-1", min=-1, max=900000,
                                    style=wx.TE_PROCESS_ENTER
                                    )
        grid_sx_Vcod.Add(self.spinMinr, 0, wx.ALL, 5)
        txtMaxr = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Max Rate (kb)')
        grid_sx_Vcod.Add(txtMaxr, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.spinMaxr = wx.SpinCtrl(self.codVpanel, wx.ID_ANY,
                                    "-1", min=-1, max=900000,
                                    style=wx.TE_PROCESS_ENTER
                                    )
        grid_sx_Vcod.Add(self.spinMaxr, 0, wx.ALL, 5)
        txtBuffer = wx.StaticText(self.codVpanel, wx.ID_ANY,
                                  'Buffer Size (kb)'
                                  )
        grid_sx_Vcod.Add(txtBuffer, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.spinBufsize = wx.SpinCtrl(self.codVpanel, wx.ID_ANY,
                                       "-1", min=-1, max=900000,
                                       style=wx.TE_PROCESS_ENTER
                                       )
        grid_sx_Vcod.Add(self.spinBufsize, 0, wx.ALL, 5)
        txtVaspect = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Aspect Ratio')
        grid_sx_Vcod.Add(txtVaspect, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_Vaspect = wx.ComboBox(self.codVpanel, wx.ID_ANY,
                                       choices=AV_Conv.ASPECTRATIO,
                                       size=(120, -1), style=wx.CB_DROPDOWN
                                       | wx.CB_READONLY,
                                       )
        grid_sx_Vcod.Add(self.cmb_Vaspect, 0, wx.ALL, 5)
        txtFps = wx.StaticText(self.codVpanel, wx.ID_ANY, 'FPS (frame rate)')
        grid_sx_Vcod.Add(txtFps, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_Fps = wx.ComboBox(self.codVpanel, wx.ID_ANY,
                                   choices=AV_Conv.FPS,
                                   size=(120, -1),
                                   style=wx.CB_DROPDOWN
                                   | wx.CB_READONLY,
                                   )
        grid_sx_Vcod.Add(self.cmb_Fps, 0, wx.ALL, 5)
        txtPixfrm = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Pixel Format')
        grid_sx_Vcod.Add(txtPixfrm, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_Pixfrm = wx.ComboBox(self.codVpanel, wx.ID_ANY,
                                      choices=AV_Conv.PIXELFRMT,
                                      size=(120, -1), style=wx.CB_DROPDOWN
                                      | wx.CB_READONLY,
                                      )
        grid_sx_Vcod.Add(self.cmb_Pixfrm, 0, wx.ALL, 5)
        txtSubmap = wx.StaticText(self.codVpanel, wx.ID_ANY, 'Subtitle Map')
        grid_sx_Vcod.Add(txtSubmap, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_Submap = wx.ComboBox(self.codVpanel, wx.ID_ANY,
                                      choices=[('None'),
                                               ('All'),
                                               ],
                                      size=(120, -1), style=wx.CB_DROPDOWN
                                      | wx.CB_READONLY,
                                      )
        grid_sx_Vcod.Add(self.cmb_Submap, 0, wx.ALL, 5)

        self.codVpanel.SetSizer(grid_sx_Vcod)  # set panel
        self.codVpanel.SetAutoLayout(1)
        self.codVpanel.SetupScrolling()
        # BOX central box
        box3 = wx.StaticBox(self.nb_Video, wx.ID_ANY, _("Optimizations"))
        self.box_opt = wx.StaticBoxSizer(box3, wx.VERTICAL)
        sizer_nbVideo.Add(self.box_opt, 1, wx.ALL | wx.EXPAND, 5)
        # panel AV1
        self.av1panel = AV1Pan(self.nb_Video, self.opt,
                               self.appdata['ostype'])
        self.box_opt.Add(self.av1panel, 0, wx.CENTRE)
        # panel vp8 vp9
        self.vp9panel = WebMPan(self.nb_Video, self.opt,
                                self.appdata['ostype'])
        self.box_opt.Add(self.vp9panel, 0, wx.CENTRE)
        # panel x/h 264 265
        self.h264panel = Hevc_Avc(self.nb_Video, self.opt,
                                  self.appdata['ostype'])
        self.box_opt.Add(self.h264panel, 0, wx.CENTRE)
        # BOX Video filters
        box4 = wx.StaticBox(self.nb_Video, wx.ID_ANY, _("Video Filters"))
        self.box_Vfilters = wx.StaticBoxSizer(box4, wx.VERTICAL)
        self.btn_preview = wx.Button(self.nb_Video, wx.ID_ANY,
                                     _("Preview"), size=(-1, -1))
        self.btn_preview.SetBitmap(bmpplay, wx.LEFT)

        self.box_Vfilters.Add(self.btn_preview, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_preview.Disable()
        self.btn_reset = wx.Button(self.nb_Video, wx.ID_ANY,
                                   _("Reset all"), size=(-1, -1))
        self.btn_reset.SetBitmap(self.bmpreset, wx.LEFT)
        self.box_Vfilters.Add(self.btn_reset, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_reset.Disable()
        lineflt = wx.StaticLine(self.nb_Video,
                                wx.ID_ANY,
                                pos=wx.DefaultPosition,
                                size=wx.DefaultSize,
                                style=wx.LI_HORIZONTAL,
                                name=wx.StaticLineNameStr,
                                )
        self.box_Vfilters.Add(lineflt, 0, wx.ALL | wx.EXPAND, 10)
        sizer_nbVideo.Add(self.box_Vfilters, 0, wx.ALL | wx.EXPAND, 5)
        self.filterVpanel = scrolled.ScrolledPanel(self.nb_Video, -1,
                                                   size=(220, 700),
                                                   style=wx.TAB_TRAVERSAL
                                                   | wx.BORDER_NONE,
                                                   name="panelscroll",
                                                   )
        sizer_Vfilter = wx.BoxSizer(wx.VERTICAL)
        self.btn_videosize = wx.Button(self.filterVpanel, wx.ID_ANY,
                                       _("Resize"), size=(-1, -1))
        self.btn_videosize.SetBitmap(bmpresize, wx.LEFT)
        sizer_Vfilter.Add(self.btn_videosize, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_crop = wx.Button(self.filterVpanel, wx.ID_ANY,
                                  _("Crop"), size=(-1, -1))
        self.btn_crop.SetBitmap(bmpcrop, wx.LEFT)
        sizer_Vfilter.Add(self.btn_crop, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_rotate = wx.Button(self.filterVpanel, wx.ID_ANY,
                                    _("Transpose"), size=(-1, -1))
        self.btn_rotate.SetBitmap(bmprotate, wx.LEFT)

        sizer_Vfilter.Add(self.btn_rotate, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_lacing = wx.Button(self.filterVpanel, wx.ID_ANY,
                                    _("Deinterlace"), size=(-1, -1))
        self.btn_lacing.SetBitmap(bmpdeinterlace, wx.LEFT)
        sizer_Vfilter.Add(self.btn_lacing, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_denois = wx.Button(self.filterVpanel, wx.ID_ANY,
                                    _("Denoise"), size=(-1, -1))
        self.btn_denois.SetBitmap(bmpdenoiser, wx.LEFT)
        sizer_Vfilter.Add(self.btn_denois, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_vidstab = wx.Button(self.filterVpanel, wx.ID_ANY,
                                     _("Stabilize"), size=(-1, -1))
        self.btn_vidstab.SetBitmap(bmpstab, wx.LEFT)
        sizer_Vfilter.Add(self.btn_vidstab, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_coloreq = wx.Button(self.filterVpanel, wx.ID_ANY,
                                     _("Equalize"), size=(-1, -1))
        self.btn_coloreq.SetBitmap(bmpcoloreq, wx.LEFT)
        sizer_Vfilter.Add(self.btn_coloreq, 0, wx.ALL | wx.EXPAND, 5)

        self.box_Vfilters.Add(self.filterVpanel, 1, wx.EXPAND)
        self.filterVpanel.SetSizer(sizer_Vfilter)  # set panel
        self.filterVpanel.SetAutoLayout(1)
        self.filterVpanel.SetupScrolling()

        self.nb_Video.SetSizer(sizer_nbVideo)
        self.notebook.AddPage(self.nb_Video, _("Video"))
        #  END NOTEBOOK PANEL 1 Video

        # -------------- BEGIN NOTEBOOK PANEL 2 Audio:
        self.nb_Audio = wx.Panel(self.notebook, wx.ID_ANY)
        sizer_nbAudio = wx.BoxSizer(wx.VERTICAL)
        sizer_codecAudio = wx.BoxSizer(wx.HORIZONTAL)
        sizer_nbAudio.Add(sizer_codecAudio, 0, wx.EXPAND)
        self.rdb_a = wx.RadioBox(self.nb_Audio, wx.ID_ANY,
                                 (_("Audio Encoder")),
                                 choices=list(AV_Conv.ACODECS.keys()),
                                 majorDimension=6, style=wx.RA_SPECIFY_COLS
                                 )
        for n, v in enumerate(AV_Conv.AV_FORMATS["mkv"]):
            if not v:  # disable only not compatible with mkv
                self.rdb_a.EnableItem(n, enable=False)
        sizer_codecAudio.Add(self.rdb_a, 1, wx.ALL | wx.EXPAND, 5)

        # BOX audio properties
        box5 = wx.StaticBox(self.nb_Audio, wx.ID_ANY, _("Audio Properties"))
        self.box_audioProper = wx.StaticBoxSizer(box5, wx.VERTICAL)
        sizer_codecAudio.Add(self.box_audioProper, 1, wx.ALL | wx.EXPAND, 5)
        sizer_a_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        self.box_audioProper.Add(sizer_a_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_aparam = wx.Button(self.nb_Audio, wx.ID_ANY,
                                    _("Settings"), size=(-1, -1))
        self.btn_aparam.SetBitmap(bmpasettings, wx.LEFT)
        sizer_a_ctrl.Add(self.btn_aparam, 0, wx.ALL
                         | wx.ALIGN_CENTER_VERTICAL, 2,
                         )
        self.txt_audio_options = wx.TextCtrl(self.nb_Audio, wx.ID_ANY,
                                             size=(-1, -1),
                                             style=wx.TE_READONLY
                                             )
        sizer_a_ctrl.Add(self.txt_audio_options, 1, wx.ALL | wx.EXPAND, 2)

        # BOX stream mapping
        msg = _("Audio Streams Mapping")
        box6 = wx.StaticBox(self.nb_Audio, wx.ID_ANY, msg)
        self.box_audioMap = wx.StaticBoxSizer(box6, wx.VERTICAL)
        sizer_nbAudio.Add(self.box_audioMap, 0, wx.ALL | wx.EXPAND, 5)
        sizer_Amap = wx.BoxSizer(wx.HORIZONTAL)
        self.box_audioMap.Add(sizer_Amap, 0, wx.ALL | wx.EXPAND, 5)
        txtAinmap = wx.StaticText(self.nb_Audio, wx.ID_ANY,
                                  _('Index Selection:')
                                  )
        sizer_Amap.Add(txtAinmap, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_A_inMap = wx.ComboBox(self.nb_Audio, wx.ID_ANY,
                                       choices=['Auto', '1', '2', '3',
                                                '4', '5', '6', '7', '8'],
                                       size=(160, -1), style=wx.CB_DROPDOWN
                                       | wx.CB_READONLY,
                                       )
        sizer_Amap.Add(self.cmb_A_inMap, 0, wx.ALL, 5)
        txtAoutmap = wx.StaticText(self.nb_Audio, wx.ID_ANY, _('Map:'))
        sizer_Amap.Add(txtAoutmap, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.cmb_A_outMap = wx.ComboBox(self.nb_Audio, wx.ID_ANY,
                                        choices=['Auto', 'All', 'Index only'],
                                        size=(160, -1),
                                        style=wx.CB_DROPDOWN
                                        | wx.CB_READONLY,
                                        )
        sizer_Amap.Add(self.cmb_A_outMap, 0, wx.ALL, 5)

        # BOX Audio Filters
        box7 = wx.StaticBox(self.nb_Audio, wx.ID_ANY, _("Audio Filters"))
        self.box_aFilters = wx.StaticBoxSizer(box7, wx.VERTICAL)
        sizer_nbAudio.Add(self.box_aFilters, 1, wx.ALL | wx.EXPAND, 5)
        sizer_a_normaliz = wx.BoxSizer(wx.VERTICAL)
        self.box_aFilters.Add(sizer_a_normaliz, 0, wx.EXPAND)

        self.btn_audio_preview = wx.Button(self.nb_Audio, wx.ID_ANY,
                                           _("Preview"), size=(-1, -1))
        self.btn_audio_preview.SetBitmap(bmpapreview, wx.LEFT)
        sizer_a_normaliz.Add(self.btn_audio_preview, 0, wx.ALL | wx.SHAPED, 5)

        self.rdbx_normalize = wx.RadioBox(self.nb_Audio, wx.ID_ANY,
                                          (_("Normalization")),
                                          choices=[('Off'),
                                                   ('PEAK'),
                                                   ('RMS'),
                                                   ('EBU R128'),
                                                   ],
                                          majorDimension=1,
                                          style=wx.RA_SPECIFY_ROWS,
                                          )
        sizer_a_normaliz.Add(self.rdbx_normalize, 0, wx.ALL | wx.EXPAND, 5)
        self.peakpanel = wx.Panel(self.nb_Audio, wx.ID_ANY,
                                  style=wx.TAB_TRAVERSAL
                                  )
        grid_peak = wx.FlexGridSizer(1, 4, 15, 4)
        sizer_a_normaliz.Add(self.peakpanel, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_voldect = wx.Button(self.peakpanel, wx.ID_ANY,
                                     _("Volume detect"), size=(-1, -1))
        self.btn_voldect.SetBitmap(bmppeaklevel, wx.LEFT)
        grid_peak.Add(self.btn_voldect, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.btn_details = wx.Button(self.peakpanel, wx.ID_ANY,
                                     _("Volume Statistics"), size=(-1, -1))
        self.btn_details.SetBitmap(bmpanalyzes, wx.LEFT)
        grid_peak.Add(self.btn_details, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.lab_amplitude = wx.StaticText(self.peakpanel, wx.ID_ANY,
                                           (_("Target level:"))
                                           )
        grid_peak.Add(self.lab_amplitude, 0, wx.LEFT
                      | wx.ALIGN_CENTER_VERTICAL, 10)
        self.spin_target = FS.FloatSpin(self.peakpanel, wx.ID_ANY,
                                        min_val=-99.0, max_val=0.0,
                                        increment=0.5, value=-1.0,
                                        agwStyle=FS.FS_LEFT, size=(120, -1)
                                        )
        self.spin_target.SetFormat("%f"), self.spin_target.SetDigits(1)
        grid_peak.Add(self.spin_target, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.peakpanel.SetSizer(grid_peak)  # set panel
        self.ebupanel = scrolled.ScrolledPanel(self.nb_Audio, -1,
                                               size=(500, 700),
                                               style=wx.TAB_TRAVERSAL
                                               | wx.BORDER_THEME,
                                               name="panelscroll",
                                               )
        grid_ebu = wx.FlexGridSizer(3, 2, 0, 0)
        sizer_a_normaliz.Add(self.ebupanel, 0, wx.ALL | wx.EXPAND, 5)
        self.lab_i = wx.StaticText(self.ebupanel, wx.ID_ANY, (
            _("Set (I) integrated loudness target")))
        grid_ebu.Add(self.lab_i, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.spin_i = FS.FloatSpin(self.ebupanel, wx.ID_ANY,
                                   min_val=-70.0, max_val=-5.0,
                                   increment=0.5, value=-16.0,
                                   agwStyle=FS.FS_LEFT, size=(120, -1)
                                   )
        self.spin_i.SetFormat("%f"), self.spin_i.SetDigits(1)
        grid_ebu.Add(self.spin_i, 0, wx.ALL, 5)

        self.lab_tp = wx.StaticText(self.ebupanel, wx.ID_ANY, (
                                    _("Set (TP) maximum true peak")))
        grid_ebu.Add(self.lab_tp, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.spin_tp = FS.FloatSpin(self.ebupanel, wx.ID_ANY,
                                    min_val=-9.0, max_val=0.0,
                                    increment=0.5, value=-1.5,
                                    agwStyle=FS.FS_LEFT, size=(120, -1)
                                    )
        self.spin_tp.SetFormat("%f"), self.spin_tp.SetDigits(1)
        grid_ebu.Add(self.spin_tp, 0, wx.ALL, 5)

        self.lab_lra = wx.StaticText(self.ebupanel, wx.ID_ANY, (
                                     _("Set (LRA) loudness range target")))
        grid_ebu.Add(self.lab_lra, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.spin_lra = FS.FloatSpin(self.ebupanel, wx.ID_ANY,
                                     min_val=1.0, max_val=20.0,
                                     increment=0.5, value=11.0,
                                     agwStyle=FS.FS_LEFT, size=(120, -1)
                                     )
        self.spin_lra.SetFormat("%f"), self.spin_lra.SetDigits(1)
        grid_ebu.Add(self.spin_lra, 0, wx.ALL, 5)

        self.ebupanel.SetSizer(grid_ebu)  # set panel
        self.ebupanel.SetAutoLayout(1)
        self.ebupanel.SetupScrolling()

        self.nb_Audio.SetSizer(sizer_nbAudio)
        self.notebook.AddPage(self.nb_Audio, _("Audio"))

        # ------------------ set layout
        self.SetSizer(sizer_base)
        self.Fit()
        self.Layout()
        # ---------------------- Tooltips
        tip = (_('Add settings to presets. You can use and manage them '
                 'directly from the Presets Manager.'))
        self.btn_saveprst.SetToolTip(tip)
        tip = (_('Available video codecs. "Copy" is not a codec but indicate '
                 'that the video stream is not to be re-encoded and allows '
                 'changing the format or other parameters'))
        self.cmb_Vcod.SetToolTip(tip)
        tip = (_('Output format. It also represents the extension of '
                 'the output file.'))
        self.cmb_Vcont.SetToolTip(tip)
        tip = (_('"Video" to save the output file as a '
                 'video; "Audio" to save as an audio file only'))
        self.cmb_Media.SetToolTip(tip)
        tip = _('It can reduce the file size, but takes longer.')
        self.ckbx_pass.SetToolTip(tip)
        tip = (_('Specifies a minimum tolerance to be used. '
                 'Set to -1 to disable this control.'))
        self.spinMinr.SetToolTip(tip)
        tip = (_('Specifies a maximum tolerance. This is '
                 'only used in conjunction with buffer size. '
                 'Set to -1 to disable this control.'))
        self.spinMaxr.SetToolTip(tip)
        tip = (_('Specifies the decoder buffer size, which determines the '
                 'variability of the output bitrate. '
                 'Set to -1 to disable this control.'))
        self.spinBufsize.SetToolTip(tip)
        tip = (_('specifies the target (average) bit rate for the encoder '
                 'to use. Higher value = higher quality. Set -1 to disable '
                 'this control.'))
        self.spin_Vbrate.SetToolTip(tip)
        tip = (_('Constant rate factor. Lower values = higher quality and '
                 'a larger file size. Set to -1 to disable this control.'))
        self.slider_CRF.SetToolTip(tip)
        tip = _('Preview video filters')
        self.btn_preview.SetToolTip(tip)
        tip = _("Clear all enabled filters ")
        self.btn_reset.SetToolTip(tip)
        tip = _('Video width and video height ratio.')
        self.cmb_Vaspect.SetToolTip(tip)
        tip = (_('Frames repeat a given number of times per second. In some '
                 'countries this is 30 for NTSC, other countries (like '
                 'Italy) use 25 for PAL'))
        self.cmb_Fps.SetToolTip(tip)
        tip = (_('Gets maximum volume and average volume data in dBFS, then '
                 'calculates the offset amount for audio normalization.'))
        self.btn_voldect.SetToolTip(tip)
        tip = (_('Limiter for the maximum peak level or the mean level '
                 '(when switch to RMS) in dBFS. From -99.0 to +0.0; default '
                 'for PEAK level is -1.0; default for RMS is -20.0'))
        self.spin_target.SetToolTip(tip)
        tip = (_('Choose an index from the available audio streams. If the '
                 'source file is a video, it is recommended to select a '
                 'numeric audio index. If the source file is an audio file, '
                 'leave this control to "Auto".'))
        self.cmb_A_inMap.SetToolTip(tip)
        tip = (_('"Auto" keeps all audio stream but processes '
                 'only the one of the selected index; "All" keeps all audio '
                 'streams and processes them all with the properties of the '
                 'selected index; "Index only" processes and keeps only the '
                 'selected index audio stream.'))
        self.cmb_A_outMap.SetToolTip(tip)
        tip = (_('Integrated Loudness Target in LUFS. '
                 'From -70.0 to -5.0, default is -24.0'))
        self.spin_i.SetToolTip(tip)
        tip = (_('Maximum True Peak in dBTP. From -9.0 '
                 'to +0.0, default is -2.0'))
        self.spin_tp.SetToolTip(tip)
        tip = (_('Loudness Range Target in LUFS. '
                 'From +1.0 to +20.0, default is +7.0'))
        self.spin_lra.SetToolTip(tip)
        tip = _('Play and listen to the result of audio filters')
        self.btn_audio_preview.SetToolTip(tip)

        # ----------------------Binding (EVT)----------------------#

        # Note: wx.EVT_TEXT_ENTER é diverso da wx.EVT_TEXT: Il primo
        # é responsivo agli input di tastiera, il secondo é responsivo
        # agli input di tastiera ma anche agli "append"

        self.Bind(wx.EVT_COMBOBOX, self.videoCodec, self.cmb_Vcod)
        self.Bind(wx.EVT_COMBOBOX, self.on_Container, self.cmb_Vcont)
        self.Bind(wx.EVT_COMBOBOX, self.on_Media, self.cmb_Media)
        self.Bind(wx.EVT_CHECKBOX, self.on_Pass, self.ckbx_pass)
        self.Bind(wx.EVT_CHECKBOX, self.on_WebOptimize, self.ckbx_web)
        self.Bind(wx.EVT_SPINCTRL, self.on_Vbitrate, self.spin_Vbrate)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.on_Crf, self.slider_CRF)
        self.Bind(wx.EVT_BUTTON, self.on_saveprst, self.btn_saveprst)
        self.Bind(wx.EVT_BUTTON, self.on_Set_scale, self.btn_videosize)
        self.Bind(wx.EVT_BUTTON, self.on_Set_crop, self.btn_crop)
        self.Bind(wx.EVT_BUTTON, self.on_Set_transpose, self.btn_rotate)
        self.Bind(wx.EVT_BUTTON, self.on_Set_deinterlace, self.btn_lacing)
        self.Bind(wx.EVT_BUTTON, self.on_Set_denoiser, self.btn_denois)
        self.Bind(wx.EVT_BUTTON, self.on_Set_stabilizer, self.btn_vidstab)
        self.Bind(wx.EVT_BUTTON, self.on_Set_coloreq, self.btn_coloreq)
        self.Bind(wx.EVT_BUTTON, self.on_video_preview, self.btn_preview)
        self.Bind(wx.EVT_BUTTON, self.on_audio_preview, self.btn_audio_preview)
        self.Bind(wx.EVT_BUTTON, self.on_FiltersClear, self.btn_reset)
        self.Bind(wx.EVT_COMBOBOX, self.on_Vaspect, self.cmb_Vaspect)
        self.Bind(wx.EVT_COMBOBOX, self.on_Vrate, self.cmb_Fps)
        self.Bind(wx.EVT_RADIOBOX, self.on_AudioCodecs, self.rdb_a)
        self.Bind(wx.EVT_BUTTON, self.on_AudioParam, self.btn_aparam)
        self.Bind(wx.EVT_COMBOBOX, self.on_audio_index, self.cmb_A_inMap)
        self.Bind(wx.EVT_COMBOBOX, self.on_audio_mapping, self.cmb_A_outMap)
        self.Bind(wx.EVT_RADIOBOX, self.onNormalize, self.rdbx_normalize)
        self.Bind(wx.EVT_SPINCTRL, self.on_enter_Ampl, self.spin_target)
        self.Bind(wx.EVT_BUTTON, self.on_Audio_analyzes, self.btn_voldect)
        self.Bind(wx.EVT_BUTTON, self.on_Show_normlist, self.btn_details)

        #  initialize default layout:
        self.rdb_a.SetSelection(0), self.cmb_Vcod.SetSelection(1)
        self.cmb_Media.SetSelection(0), self.cmb_Vcont.SetSelection(0)
        self.cmb_Fps.SetSelection(0), self.cmb_Vaspect.SetSelection(0)
        self.cmb_Pixfrm.SetSelection(7), self.cmb_Submap.SetSelection(1)
        self.cmb_A_outMap.SetSelection(0), self.cmb_A_inMap.SetSelection(0)
        self.cmb_A_outMap.Disable()
        self.UI_set()
        self.audio_default()
        self.normalize_default()
        pub.subscribe(self.reset_on_changed_data, "RESET_ON_CHANGED_LIST")
    # -------------------------------------------------------------------#

    def reset_on_changed_data(self, msg):
        """
        This method is called using pub/sub protocol
        """
        if not self.rdbx_normalize.GetSelection() == 0:
            self.normalize_default(self)
        if self.opt["VFilters"]:
            self.on_FiltersClear(self)
    # -------------------------------------------------------------------#

    def UI_set(self):
        """
        Update all the panel controls.
        """
        if self.opt["VideoCodec"] in ["-c:v libx264", "-c:v libx265"]:
            self.vp9panel.Hide(), self.av1panel.Hide(), self.h264panel.Show()
            self.h264panel.default()

            if self.opt["VideoCodec"] == "-c:v libx264":
                self.slider_CRF.SetValue(23), self.spin_Vbrate.SetValue(1500)

            elif self.opt["VideoCodec"] == "-c:v libx265":
                self.slider_CRF.SetValue(28), self.spin_Vbrate.SetValue(1500)

            self.filterVpanel.Enable(), self.slider_CRF.SetMax(51)

        elif self.opt["VideoCodec"] in ["-c:v libvpx", "-c:v libvpx-vp9"]:
            self.vp9panel.Show(), self.h264panel.Hide(), self.av1panel.Hide()
            self.vp9panel.default()
            self.slider_CRF.SetMax(63)
            self.slider_CRF.SetValue(31), self.spin_Vbrate.SetValue(0)
            self.filterVpanel.Enable(), self.nb_Video.Layout()

        elif self.opt["VideoCodec"] == "-c:v libaom-av1":
            self.vp9panel.Hide(), self.h264panel.Hide(), self.av1panel.Show()
            self.av1panel.default()
            self.slider_CRF.SetMax(63)
            self.slider_CRF.SetValue(31), self.spin_Vbrate.SetValue(0)
            self.filterVpanel.Enable(), self.nb_Video.Layout()

        elif self.opt["VideoCodec"] == "-c:v copy":
            self.slider_CRF.SetValue(-1), self.spin_Vbrate.SetValue(-1)
            self.vp9panel.Hide(), self.h264panel.Hide(), self.av1panel.Hide()
            self.filterVpanel.Disable(), self.on_FiltersClear(self)

        else:  # all others containers that not use h264
            self.slider_CRF.SetValue(-1), self.spin_Vbrate.SetValue(1500)
            self.vp9panel.Hide(), self.h264panel.Hide(), self.av1panel.Hide()
            self.filterVpanel.Enable()

        if self.rdbx_normalize.GetSelection() == 3:
            self.ckbx_pass.SetValue(True)
            self.ckbx_pass.Disable()
        else:
            if self.opt["VideoCodec"] == "-c:v copy":
                self.ckbx_pass.SetValue(False)
                self.ckbx_pass.Disable()
            else:
                self.ckbx_pass.Enable()
        self.on_Pass(self)
    # -------------------------------------------------------------------#

    def audio_default(self):
        """
        Set default audio parameters. This method is called at
        start-up and whenever changes the video container selection.
        """
        self.rdb_a.SetStringSelection("Auto")
        self.opt["AudioCodStr"] = "Auto"
        self.opt["AudioCodec"] = ["", ""]
        self.opt["AudioBitrate"] = ["", ""]
        self.opt["AudioChannel"] = ["", ""]
        self.opt["AudioRate"] = ["", ""]
        self.opt["AudioDepth"] = ["", ""]
        self.btn_aparam.Disable()
        self.btn_aparam.SetBackgroundColour(wx.NullColour)
        self.txt_audio_options.Clear()
        # self.rdbx_normalize.Enable()
    # -------------------------------------------------------------------#

    def normalize_default(self, setoff=True):
        """
        Reset normalization parameters on the audio properties.
        This method even is called by `MainFrame.switch_video_conv()`
        on start-up and when there are changing on `dragNdrop` panel.
        """
        if setoff:
            self.rdbx_normalize.SetSelection(0)
        if not self.btn_voldect.IsEnabled():
            self.btn_voldect.Enable()
        self.spin_target.SetValue(-1.0)
        self.peakpanel.Hide(), self.ebupanel.Hide(), self.btn_details.Hide()
        self.opt["PEAK"], self.opt["EBU"], self.opt["RMS"] = [], "", []

    # ----------------------Event handler (callback)----------------------#

    def videoCodec(self, event):
        """
        This event triggers the setting to the default values.
        """
        selected = AV_Conv.VCODECS.get(self.cmb_Vcod.GetValue())
        libcodec = list(selected.keys())[0]
        self.cmb_Vcont.Clear()
        for f in selected.values():
            self.cmb_Vcont.Append((f),)
        self.cmb_Vcont.SetSelection(0)

        self.opt["VideoCodec"] = libcodec
        self.opt["VidCmbxStr"] = self.cmb_Vcod.GetValue()
        self.opt["OutputFormat"] = self.cmb_Vcont.GetValue()
        self.opt["VideoBitrate"] = ""
        self.opt["CRF"] = ""

        if self.cmb_Vcod.GetValue() == "Copy":
            self.spinMinr.Disable(), self.spinMaxr.Disable()
            self.spinBufsize.Disable()
            self.opt["Passing"] = "1 pass"
        else:
            self.spinMinr.Enable(), self.spinMaxr.Enable()
            self.spinBufsize.Enable()

        self.UI_set()
        self.audio_default()  # reset audio radiobox and dict
        self.setAudioRadiobox(self)
    # ------------------------------------------------------------------#

    def on_Media(self, event):
        """
        Combobox Media Sets layout to Audio or Video formats
        """
        if self.cmb_Media.GetValue() == 'Audio':
            self.cmb_Vcod.SetSelection(6)
            self.opt["VideoCodec"] = "-c:v copy"
            self.audio_default()
            self.codVpanel.Disable()
            self.cmb_Vcont.Clear()
            for f in AV_Conv.A_FORMATS:
                self.cmb_Vcont.Append((f),)
            self.cmb_Vcont.SetSelection(0)
            self.UI_set()
            self.setAudioRadiobox(self)

        elif self.cmb_Media.GetValue() == 'Video':
            self.codVpanel.Enable()
            self.cmb_Vcod.SetSelection(1)
            self.videoCodec(self)

        self.opt["OutputFormat"] = self.cmb_Vcont.GetValue()
    # ------------------------------------------------------------------#

    def on_Container(self, event):
        """
        Appends on container combobox according to audio and video formats
        """
        if self.cmb_Vcont.GetValue() == "Copy":
            self.opt["OutputFormat"] = ''
        else:
            self.opt["OutputFormat"] = self.cmb_Vcont.GetValue()
        self.setAudioRadiobox(self)
    # ------------------------------------------------------------------#

    def on_WebOptimize(self, event):
        """
        Adds or removes -movflags faststart flag to maximize
        speed on video streaming.
        """
        check = self.ckbx_web.IsChecked()
        self.opt["WebOptim"] = '-movflags faststart' if check else ''
    # ------------------------------------------------------------------#

    def on_Pass(self, event):
        """
        enable or disable operations for two pass encoding
        """
        if self.ckbx_pass.IsChecked():
            self.opt["Passing"] = "2 pass"
            if self.opt["VideoCodec"] in ["-c:v libvpx", "-c:v libvpx-vp9",
                                          "-c:v libaom-av1"]:
                self.slider_CRF.Enable()
                self.spin_Vbrate.Enable()

            elif self.opt["VideoCodec"] == "-c:v copy":
                self.slider_CRF.Disable()
                self.spin_Vbrate.Disable()
            else:
                self.slider_CRF.Disable()
                self.spin_Vbrate.Enable()
            self.on_FiltersClear(self, True)  # disable vidstab
        else:
            self.opt["Passing"] = "1 pass"
            if self.opt["VideoCodec"] in ["-c:v libx264", "-c:v libx265"]:
                if self.slider_CRF.GetValue() == -1:
                    self.spin_Vbrate.Enable()
                else:
                    self.spin_Vbrate.Disable()
                self.slider_CRF.Enable()

            elif self.opt["VideoCodec"] in ["-c:v libvpx", "-c:v libvpx-vp9",
                                            "-c:v libaom-av1"]:
                self.slider_CRF.Enable()
                self.spin_Vbrate.Enable()

            elif self.opt["VideoCodec"] == "-c:v copy":
                self.slider_CRF.Disable()
                self.spin_Vbrate.Disable()
            else:
                self.slider_CRF.Disable()
                self.spin_Vbrate.Enable()
    # ------------------------------------------------------------------#

    def on_Vbitrate(self, event):
        """
        Here the bitrate values are set.
        Some codec do not support setting both bitrate
        and CRF, especially if two-pass is enabled.
        """
        val = self.spin_Vbrate.GetValue()

        if self.opt["VideoCodec"] not in ["-c:v libvpx", "-c:v libvpx-vp9",
                                          "-c:v libaom-av1"]:
            self.opt["CRF"] = ""

        self.opt["VideoBitrate"] = "" if val == -1 else f"-b:v {val}k"
    # ------------------------------------------------------------------#

    def on_Crf(self, event):
        """
        Here the CRF values are set.
        Some codec do not support setting both bitrate
        and CRF, especially if two-pass is enabled.
        """
        val = self.slider_CRF.GetValue()
        if self.opt["VideoCodec"] not in ["-c:v libvpx", "-c:v libvpx-vp9",
                                          "-c:v libaom-av1"]:
            self.opt["VideoBitrate"] = ""

            if val == -1:
                self.spin_Vbrate.Enable()
            else:
                self.spin_Vbrate.Disable()

        self.opt["CRF"] = "" if val == -1 else f"-crf {val}"

    # ------------------------------------------------------------------#

    def on_audio_preview(self, event):
        """
        It allows a direct evaluation of the sound results given
        by the audio filters with the ability to playback even the
        selected audio streams through audio index mapping.
        """
        def _undetect():
            wx.MessageBox(_('Undetected volume values! Click the '
                            '"Volume detect" button to analyze '
                            'audio volume data.'),
                          'Videomass', wx.ICON_INFORMATION, self
                          )
        fget = self.file_selection()
        if not fget or not self.get_audio_stream(fget):
            return None

        if self.cmb_A_inMap.GetValue() == 'Auto':
            idx = ''
        else:
            idx = f'-ast a:{str(int(self.cmb_A_inMap.GetValue()) - 1)}'

        if self.rdbx_normalize.GetSelection() == 0:
            afilter = ''

        elif self.rdbx_normalize.GetSelection() == 1:
            if self.btn_voldect.IsEnabled():
                return _undetect()
            afilter = f'-af {self.opt["PEAK"][fget[1]][5].split()[1]}'

        elif self.rdbx_normalize.GetSelection() == 2:
            if self.btn_voldect.IsEnabled():
                return _undetect()
            afilter = f'-af {self.opt["RMS"][fget[1]][5].split()[1]}'

        elif self.rdbx_normalize.GetSelection() == 3:
            afilter = (f'-af loudnorm=I={str(self.spin_i.GetValue())}'
                       f':LRA={str(self.spin_lra.GetValue())}'
                       f':TP={str(self.spin_tp.GetValue())}')

        if self.parent.checktimestamp:
            args = (f'-showmode waves -vf "{self.parent.cmdtimestamp}" '
                    f'{afilter} {idx}')
        else:
            args = f'{afilter} {idx}'

        stream_play(self.parent.file_src[fget[1]],
                    self.parent.time_seq,
                    args,
                    self.parent.autoexit
                    )
        return None
    # ------------------------------------------------------------------#

    def on_video_preview(self, event):
        """
        Showing selected video preview with applied filters.
        Note that libstab filter is not possible to preview.
        """
        fget = self.file_selection()
        if not fget or not self.opt["VFilters"]:
            return
        if self.opt["Vidstabtransform"]:
            wx.MessageBox(_("Unable to preview Video Stabilizer filter"),
                          "Videomass", wx.ICON_INFORMATION, self)
            return

        flt = self.opt["VFilters"]
        if self.parent.checktimestamp:
            flt = f'{flt},"{self.parent.cmdtimestamp}"'

        stream_play(self.parent.file_src[fget[1]],
                    self.parent.time_seq,
                    flt,
                    self.parent.autoexit
                    )
    # ------------------------------------------------------------------#

    def on_FiltersClear(self, event, disablevidstab=False):
        """
        Reset all enabled filters. If default disablevidstab
        arg is True, it disable only vidstab filter values.
        """
        if disablevidstab:
            self.opt["Vidstabtransform"], self.opt["Unsharp"] = "", ""
            self.opt["Vidstabdetect"], self.opt["Makeduo"] = "", False
            self.chain_all_video_filters()
            self.btn_vidstab.SetBackgroundColour(wx.NullColour)
            return

        if self.opt["VFilters"]:
            self.opt['Crop'], self.opt["Orientation"] = "", ["", ""]
            self.opt['Scale'], self.opt['Setdar'] = "", ""
            self.opt['Setsar'], self.opt['Deinterlace'] = "", ""
            self.opt['Interlace'], self.opt['Denoiser'] = "", ""
            self.opt["Vidstabtransform"], self.opt["Unsharp"] = "", ""
            self.opt["Vidstabdetect"], self.opt["Makeduo"] = "", False
            self.opt["VFilters"], self.opt["ColorEQ"] = "", ""

            self.btn_videosize.SetBackgroundColour(wx.NullColour)
            self.btn_crop.SetBackgroundColour(wx.NullColour)
            self.btn_denois.SetBackgroundColour(wx.NullColour)
            self.btn_lacing.SetBackgroundColour(wx.NullColour)
            self.btn_rotate.SetBackgroundColour(wx.NullColour)
            self.btn_vidstab.SetBackgroundColour(wx.NullColour)
            self.btn_coloreq.SetBackgroundColour(wx.NullColour)
            self.btn_preview.Disable()
            self.btn_reset.Disable()
    # ------------------------------------------------------------------#

    def file_selection(self):
        """
        Gets the selected file on queued files and returns an object
        of type list [str('selected file name'), int(index)].
        Returns None if no files are selected.

        """
        if len(self.parent.file_src) == 1:
            return (self.parent.file_src[0], 0)

        if not self.parent.filedropselected:
            wx.MessageBox(_("A target file must be selected in the "
                            "queued files"),
                          'Videomass', wx.ICON_INFORMATION, self)
            return None

        clicked = self.parent.filedropselected
        return (clicked, self.parent.file_src.index(clicked))
    # ------------------------------------------------------------------#

    def get_audio_stream(self, fileselected):
        """
        Given a selected media file (object of type `file_selection()`),
        it evaluates whether it contains any audio streams and any
        indexes based on selected index (audio map).
        If no audio streams or no audio index it Returns None,
        True otherwise.
        See `on_audio_preview()` method for usage.

        """
        selected = self.parent.data_files[fileselected[1]].get('streams')
        isaudio = [a for a in selected if 'audio' in a.get('codec_type')]

        if isaudio:
            if not self.cmb_A_inMap.GetValue() == 'Auto':  # 1 to 8
                if [v for v in selected if 'video' in v.get('codec_type')]:
                    idx = int(self.cmb_A_inMap.GetValue())
                else:
                    idx = int(self.cmb_A_inMap.GetValue()) - 1
                if not [x for x in isaudio if x.get('index') == idx]:
                    wx.MessageBox(_('Selected index does not exist or '
                                    'does not contain any audio streams'),
                                  'Videomass', wx.ICON_INFORMATION, self)
                    return None
        else:
            wx.MessageBox(_('ERROR: Missing audio stream:\n"{}"'
                            ).format(fileselected[0]),
                          'Videomass', wx.ICON_ERROR, self)
            return None

        return True
    # ------------------------------------------------------------------#

    def get_video_stream(self):
        """
        Given a frame or a video file, it returns a dict object
        containing required video parameters as width, height, etc.
        """
        fget = self.file_selection()
        if not fget:
            return None

        index = self.parent.data_files[fget[1]]

        if 'video' in index.get('streams')[0]['codec_type']:
            width = int(index['streams'][0]['width'])
            height = int(index['streams'][0]['height'])
            filename = index['format']['filename']
            duration = index['format'].get('time', '00:00:00.000')
            if not width or not height:
                wx.MessageBox(_('Unsupported file:\n'
                                'Missing decoder or library? '
                                'Check FFmpeg configuration.'),
                              'Videomass', wx.ICON_WARNING, self)
                self.on_FiltersClear(self)
                return None
            return dict(zip(['width', 'height', 'filename', 'duration'],
                            [width, height, filename, duration]))

        wx.MessageBox(_('The file is not a frame or a video file'),
                      'Videomass', wx.ICON_WARNING, self)
        self.on_FiltersClear(self)
        return None
    # ------------------------------------------------------------------#

    def chain_all_video_filters(self):
        """
        Concatenate all video filters enabled and sorts
        them according to an consistance ffmpeg syntax.
        """
        orderf = (self.opt['Deinterlace'], self.opt['Interlace'],
                  self.opt["Denoiser"], self.opt["Vidstabtransform"],
                  self.opt["Unsharp"], self.opt['Crop'], self.opt['Scale'],
                  self.opt["Setdar"], self.opt["Setsar"],
                  self.opt['Orientation'][0], self.opt["ColorEQ"],
                  )  # do not change the order of the filters on this tuple
        filters = ''.join([f'{x},' for x in orderf if x])[:-1]

        if filters:
            self.opt["VFilters"] = f"-vf {filters}"
            self.btn_preview.Enable(), self.btn_reset.Enable()
        else:
            self.opt["VFilters"] = ""
            self.btn_preview.Disable(), self.btn_reset.Disable()
    # ------------------------------------------------------------------#

    def on_Set_scale(self, event):
        """
        Enable or disable scale, setdar and setsar filters
        """
        kwa = self.get_video_stream()
        if not kwa:
            return

        with Scale(self,
                   self.opt["Scale"],
                   self.opt["Setdar"],
                   self.opt["Setsar"],
                   self.bmpreset,
                   **kwa,
                   ) as sizing:
            if sizing.ShowModal() == wx.ID_OK:
                data = sizing.getvalue()
                if not [x for x in data.values() if x]:
                    self.btn_videosize.SetBackgroundColour(wx.NullColour)
                    self.opt["Setdar"] = ""
                    self.opt["Setsar"] = ""
                    self.opt["Scale"] = ""
                else:
                    self.btn_videosize.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    self.opt["Scale"] = data['scale']
                    self.opt['Setdar'] = data['setdar']
                    self.opt['Setsar'] = data['setsar']

                self.chain_all_video_filters()
    # -----------------------------------------------------------------#

    def on_Set_transpose(self, event):
        """
        Enable or disable transpose filter for frame rotations
        """
        kwa = self.get_video_stream()
        if not kwa:
            return

        with Transpose(self,
                       self.opt["Orientation"][0],
                       self.opt["Orientation"][1],
                       self.bmpreset,
                       **kwa,
                       ) as rotate:
            if rotate.ShowModal() == wx.ID_OK:
                data = rotate.getvalue()
                self.opt["Orientation"][0] = data[0]  # cmd option
                self.opt["Orientation"][1] = data[1]  # msg
                if not data[0]:
                    self.btn_rotate.SetBackgroundColour(wx.NullColour)
                else:
                    self.btn_rotate.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Set_crop(self, event):
        """
        Enable or disable crop filter
        """
        kwa = self.get_video_stream()
        if not kwa:
            return

        with Crop(self, self.opt["Crop"], self.opt["CropColor"],
                  self.bmpreset, **kwa) as crop:
            if crop.ShowModal() == wx.ID_OK:
                data = crop.getvalue()
                if not data:
                    self.btn_crop.SetBackgroundColour(wx.NullColour)
                    self.opt["Crop"] = ''
                    self.opt["CropColor"] = ''
                else:
                    self.btn_crop.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    self.opt["Crop"] = f'crop={data[0]}'
                    self.opt["CropColor"] = data[1]
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Set_deinterlace(self, event):
        """
        Enable or disable filter for deinterlacing
        (w3fdif and yadif) and interlace filter.
        """
        sdf = self.get_video_stream()
        if not sdf:
            return

        with Deinterlace(self,
                         self.opt["Deinterlace"],
                         self.opt["Interlace"],
                         self.bmpreset,
                         ) as lacing:
            if lacing.ShowModal() == wx.ID_OK:
                data = lacing.getvalue()
                if not data:
                    self.btn_lacing.SetBackgroundColour(wx.NullColour)
                    self.opt["Deinterlace"] = ''
                    self.opt["Interlace"] = ''
                else:
                    self.btn_lacing.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    if 'deinterlace' in data:
                        self.opt["Deinterlace"] = data["deinterlace"]
                        self.opt["Interlace"] = ''
                    elif 'interlace' in data:
                        self.opt["Interlace"] = data["interlace"]
                        self.opt["Deinterlace"] = ''
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Set_denoiser(self, event):
        """
        Enable or disable denoiser filters (nlmeans and hqdn3d)
        useful in some case, i.e. when apply a deinterlace filter.
        <https://askubuntu.com/questions/866186/how-to-get-good-quality-when-
        converting-digital-video>
        """
        sdf = self.get_video_stream()
        if not sdf:
            return
        with Denoisers(self, self.opt["Denoiser"], self.bmpreset) as den:
            if den.ShowModal() == wx.ID_OK:
                data = den.getvalue()
                if not data:
                    self.btn_denois.SetBackgroundColour(wx.NullColour)
                    self.opt["Denoiser"] = ''
                else:
                    self.btn_denois.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    self.opt["Denoiser"] = data
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Set_stabilizer(self, event):
        """
        Enable or disable libvidstab filter for video stabilization.
        Note, this filter is incompatible with 2 pass encoding that
        includes `-pass 1` and` -pass 2` ffmpeg args/options.
        """
        sdf = self.get_video_stream()
        if not sdf:
            return
        if self.opt["Passing"] == "2 pass":
            wx.MessageBox(_('This filter is incompatible with '
                            '2-pass enabled'),
                          'Videomass', wx.ICON_INFORMATION, self)
            return

        with VidstabSet(self,
                        self.opt["Vidstabdetect"],
                        self.opt["Vidstabtransform"],
                        self.opt["Unsharp"],
                        self.opt["Makeduo"],
                        self.bmpreset,
                        **sdf,
                        ) as stab:
            if stab.ShowModal() == wx.ID_OK:
                data = stab.getvalue()
                if not data:
                    self.btn_vidstab.SetBackgroundColour(wx.NullColour)
                    self.opt["Vidstabdetect"] = ""
                    self.opt["Vidstabtransform"] = ""
                    self.opt["Unsharp"] = ""
                    self.opt["Makeduo"] = False
                else:
                    self.btn_vidstab.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    self.opt["Vidstabdetect"] = data[0]
                    self.opt['Vidstabtransform'] = data[1]
                    self.opt['Unsharp'] = data[2]
                    self.opt["Makeduo"] = data[3]
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Set_coloreq(self, event):
        """
        Enable or disable color correction filter like
        contrast, brightness, saturation, gamma.
        """
        kwa = self.get_video_stream()
        if not kwa:
            return
        with ColorEQ(self, self.opt["ColorEQ"], self.bmpreset, **kwa,
                     ) as coloreq:
            if coloreq.ShowModal() == wx.ID_OK:
                data = coloreq.getvalue()
                if not data:
                    self.btn_coloreq.SetBackgroundColour(wx.NullColour)
                    self.opt["ColorEQ"] = ''
                else:
                    self.btn_coloreq.SetBackgroundColour(
                        wx.Colour(AV_Conv.VIOLET))
                    self.opt["ColorEQ"] = data
                self.chain_all_video_filters()
    # ------------------------------------------------------------------#

    def on_Vaspect(self, event):
        """
        Set aspect parameter (16:9, 4:3)
        """
        if self.cmb_Vaspect.GetValue() == "Auto":
            self.opt["AspectRatio"] = ""

        else:
            self.opt["AspectRatio"] = f'-aspect {self.cmb_Vaspect.GetValue()}'
    # ------------------------------------------------------------------#

    def on_Vrate(self, event):
        """
        Set video rate parameter with fps values
        """
        fps = self.cmb_Fps.GetValue()
        if fps == "Auto":
            self.opt["FPS"] = ""
        else:
            self.opt["FPS"] = f"-r {fps}"
    # ------------------------------------------------------------------#

    def setAudioRadiobox(self, event):
        """
        Container combobox sets compatible audio codecs
        for the selected format. See AV_FORMATS dict

        """
        if self.cmb_Media.GetValue() == 'Video':
            if self.cmb_Vcod.GetValue() == 'Copy':  # enable all codec
                for n in range(self.rdb_a.GetCount()):
                    self.rdb_a.EnableItem(n, enable=True)
            else:
                for n, v in enumerate(AV_Conv.AV_FORMATS[
                        self.cmb_Vcont.GetValue()]):
                    if v:
                        self.rdb_a.EnableItem(n, enable=True)
                    else:
                        self.rdb_a.EnableItem(n, enable=False)
            self.rdb_a.SetSelection(0)

        if self.cmb_Media.GetValue() == 'Audio':
            for n, v in enumerate(AV_Conv.AV_FORMATS[
                    self.cmb_Vcont.GetValue()]):
                if v:
                    self.rdb_a.EnableItem(n, enable=True)
                    # self.rdb_a.SetSelection(n)
                else:
                    self.rdb_a.EnableItem(n, enable=False)
            for x in range(self.rdb_a.GetCount()):
                if self.rdb_a.IsItemEnabled(x):
                    self.rdb_a.SetSelection(x)
                    break
            self.on_AudioCodecs(self)
    # ------------------------------------------------------------------#

    def on_AudioCodecs(self, event):
        """
        choosing an item on audio radiobox list, sets the
        audio format name and the appropriate command arg,
        (see ACODECS dict), resets the audio normalize and
        some `self.opt` keys.
        """
        audiocodec = self.rdb_a.GetStringSelection()

        def _param(enablenormalization, enablebuttonparameters):
            self.opt["AudioBitrate"] = ["", ""]
            self.opt["AudioChannel"] = ["", ""]
            self.opt["AudioRate"] = ["", ""]
            self.opt["AudioDepth"] = ["", ""]

            if enablenormalization:
                self.rdbx_normalize.Enable()
            else:
                self.rdbx_normalize.Disable()
            if enablebuttonparameters:
                self.btn_aparam.Enable()
                self.txt_audio_options.SetValue('')
                self.btn_aparam.SetBackgroundColour(wx.NullColour)
            else:
                self.btn_aparam.Disable(),
                self.txt_audio_options.SetValue('')
                self.btn_aparam.SetBackgroundColour(wx.NullColour)

        # --------------------------------------------------------
        for k, v in AV_Conv.ACODECS.items():
            if audiocodec in k:
                if audiocodec == "Auto":
                    self.audio_default()
                    self.rdbx_normalize.Enable()
                    self.opt["AudioCodec"] = ["", ""]

                elif audiocodec == "Copy":
                    self.normalize_default()
                    _param(False, False)
                    amap = f'-c:a:{self.opt["AudioMap"][1]}'
                    self.opt["AudioCodec"] = [amap, v]

                elif audiocodec == _("No Audio"):
                    self.normalize_default()
                    self.opt["AudioCodec"] = ["", v]
                    _param(False, False)

                    # break
                else:
                    _param(True, True)
                    amap = f'-c:a:{self.opt["AudioMap"][1]}'
                    self.opt["AudioCodec"] = [amap, v]

                self.opt["AudioCodStr"] = audiocodec

        if audiocodec == 'No Audio':  # audio Mapping disable
            self.cmb_A_inMap.Disable()
            self.cmb_A_outMap.Disable()
            self.opt["AudioMap"] = ["", ""]
            self.opt["AudioIndex"] = ""
        else:
            self.cmb_A_inMap.Enable()
            self.on_audio_index(self)
    # -------------------------------------------------------------------#

    def on_AudioParam(self, event):
        """
        Event by Audio options button. Set audio codec string and audio
        command string and pass it to audio_dialogs method.
        """
        pcm = ["pcm_s16le", "pcm_s24le", "pcm_s32le"]

        if self.opt["AudioCodec"][1] in pcm:
            self.audio_dialog(self.opt["AudioCodStr"],
                              f'{self.opt["AudioCodStr"]} Audio Settings')
        else:
            self.audio_dialog(self.opt["AudioCodStr"],
                              f'{self.opt["AudioCodStr"]} Audio Settings')
    # -------------------------------------------------------------------#

    def audio_dialog(self, codecname, caption):
        """
        Given an audio codec specified by `codecname`,
        show a dialog for setting audio parameters
        related to the codec.
        """
        with audiodialogs.AudioSettings(self,
                                        codecname,
                                        caption,
                                        self.opt["AudioRate"],
                                        self.opt["AudioDepth"],
                                        self.opt["AudioBitrate"],
                                        self.opt["AudioChannel"],
                                        ) as audiodialog:
            if audiodialog.ShowModal() == wx.ID_OK:
                aparam = audiodialog.getvalue()
            else:
                return

        self.opt["AudioChannel"] = aparam[0]
        self.opt["AudioRate"] = aparam[1]
        self.opt["AudioBitrate"] = aparam[2]
        if codecname == 'PCM':  # wav, aiff, etc
            amap = f'-c:a:{self.opt["AudioMap"][1]}'
            if 'Auto' in aparam[3][0]:  # [3] bit depth tuple
                self.opt["AudioCodec"] = [amap, "pcm_s16le"]
            else:
                self.opt["AudioCodec"] = [amap, aparam[3][1]]
            self.opt["AudioDepth"] = (f"{aparam[3][0]}", '')  # none
        else:  # all, except PCM
            self.opt["AudioDepth"] = aparam[3]

        self.txt_audio_options.Clear()
        count = 0
        for descr in (self.opt["AudioRate"],
                      aparam[3],
                      self.opt["AudioBitrate"],
                      self.opt["AudioChannel"],
                      ):
            if descr[1]:
                count += 1
                self.txt_audio_options.AppendText(f" {descr[0]} | ")

        if count == 0:
            self.btn_aparam.SetBackgroundColour(wx.NullColour)
        else:
            self.btn_aparam.SetBackgroundColour(wx.Colour(AV_Conv.VIOLET))
        return
    # ------------------------------------------------------------------#

    def on_audio_index(self, event):
        """
        Set a specific index from audio streams.
        See: <http://ffmpeg.org/ffmpeg.html#Advanced-options>
        """
        if self.cmb_A_inMap.GetValue() == 'Auto':
            self.cmb_A_outMap.Disable()
            self.opt["AudioIndex"] = ''
        else:
            self.cmb_A_outMap.Enable()
            idx = str(int(self.cmb_A_inMap.GetValue()) - 1)
            self.opt["AudioIndex"] = f'-map 0:a:{idx}'

        self.on_audio_mapping(self)
    # ------------------------------------------------------------------#

    def on_audio_mapping(self, event):
        """
        Set the mapping of the audio streams.
        """
        index = self.cmb_A_inMap.GetValue()
        sel = self.cmb_A_outMap.GetValue()
        idx = '' if index == 'Auto' else str(int(index) - 1)

        if sel == 'Auto':
            if self.cmb_Media.GetValue() == 'Video':
                self.opt["AudioMap"] = ['-map 0:a:?', idx]

            elif self.cmb_Media.GetValue() == 'Audio':
                self.opt["AudioMap"] = [f'-map 0:a:{idx}?', '']

        elif sel == 'All':
            self.opt["AudioMap"] = ['-map 0:a:?', '']

        elif sel == 'Index only':
            self.opt["AudioMap"] = [f'-map 0:a:{idx}?', '']

        if self.opt["AudioCodec"][0]:
            self.opt["AudioCodec"][0] = f"-c:a:{self.opt['AudioMap'][1]}"

        if self.rdbx_normalize.GetSelection() in [1, 2]:
            if not self.btn_voldect.IsEnabled():
                self.btn_voldect.Enable()
    # ------------------------------------------------------------------#

    def onNormalize(self, event):
        """
        Enable or disable functionality for volume normalization.
        """
        msg_1 = (_('Activate peak level normalization, which will produce '
                   'a maximum peak level equal to the set target level.'
                   ))
        msg_2 = (_('Activate RMS-based normalization, which according to '
                   'mean volume calculates the amount of gain to reach same '
                   'average power signal.'
                   ))
        msg_3 = (_('Activate two passes normalization. It Normalizes the '
                   'perceived loudness using the \"loudnorm\" filter, which '
                   'implements the EBU R128 algorithm.'))
        if self.rdbx_normalize.GetSelection() == 1:  # is checked
            self.normalize_default(False)
            self.parent.statusbar_msg(msg_1, AV_Conv.AZURE, AV_Conv.BLACK)
            self.peakpanel.Show()

        elif self.rdbx_normalize.GetSelection() == 2:
            self.normalize_default(False)
            self.parent.statusbar_msg(msg_2, AV_Conv.TROPGREEN, AV_Conv.BLACK)
            self.peakpanel.Show(), self.spin_target.SetValue(-20)

        elif self.rdbx_normalize.GetSelection() == 3:
            self.parent.statusbar_msg(msg_3, AV_Conv.LIMEGREEN, AV_Conv.BLACK)
            self.normalize_default(False)
            self.ebupanel.Show()
            self.ckbx_pass.SetValue(True), self.ckbx_pass.Disable()
            self.opt["Passing"] = "2 pass"
            if not self.cmb_Vcod.GetSelection() == 6:  # copycodec
                self.on_Pass(self)
        else:
            self.parent.statusbar_msg(_("Audio normalization off"), None)
            self.normalize_default(False)

        self.nb_Audio.Layout()

        if not self.rdbx_normalize.GetSelection() == 3:
            if not self.cmb_Vcod.GetSelection() == 6:  # copycodec
                self.ckbx_pass.Enable()

        if self.cmb_Vcod.GetSelection() == 6:  # copycodec
            if not self.rdbx_normalize.GetSelection() == 3:
                self.ckbx_pass.SetValue(False)
    # ------------------------------------------------------------------#

    def on_enter_Ampl(self, event):
        """
        when spin_amplitude is changed enable 'Volumedetect' to
        update new incomming

        """
        if not self.btn_voldect.IsEnabled():
            self.btn_voldect.Enable()
    # ------------------------------------------------------------------#

    def on_Audio_analyzes(self, event):
        """
        Clicking on the "Detect Volume" button performs the
        PEAK/RMS-based volume detection and analysis process
        required to calculate the offset for audio volume
        normalization in dBFS:
            - PEAK-based Analyzes, get the MAXIMUM peak level data.
            - RMS-based Analyzes, get the MEAN peak level data.
        <https://superuser.com/questions/323119/how-can-i-normalize-audio-
        using-ffmpeg?utm_medium=organic>
        """
        data = volume_detect_process(self.parent.file_src,
                                     self.parent.time_seq,  # from -ss to -t
                                     self.opt["AudioIndex"],
                                     parent=self.GetParent(),
                                     )
        if data[1]:
            wx.MessageBox(f"{data[1]}", "Videomass", wx.ICON_ERROR, self)
            return

        if self.rdbx_normalize.GetSelection() == 1:  # PEAK
            target = "PEAK"
        elif self.rdbx_normalize.GetSelection() == 2:  # RMS
            target = "RMS"

        del self.opt["PEAK"][:]
        del self.opt["RMS"][:]

        gain = self.spin_target.GetValue()
        for filename, vol in zip(self.parent.file_src, data[0]):
            dataref = get_volume_data(filename,
                                      vol,
                                      gain=gain,
                                      target=target,
                                      audiomap=self.opt["AudioMap"][1],
                                      )
            self.opt[target].append(dataref)

        self.btn_voldect.Disable()
        self.btn_details.Show()
        self.nb_Audio.Layout()
    # ------------------------------------------------------------------#

    def on_Show_normlist(self, event):
        """
        Show a wx.ListCtrl dialog with volumedetect data
        """
        if self.parent.audivolnormalize:
            self.parent.audivolnormalize.Raise()
            return

        if self.rdbx_normalize.GetSelection() == 1:  # PEAK
            title = _('PEAK-based volume statistics')
        elif self.rdbx_normalize.GetSelection() == 2:  # RMS
            title = _('RMS-based volume statistics')

        if self.btn_voldect.IsEnabled():
            self.on_Audio_analyzes(self)

        lev = self.opt["RMS"] if not self.opt["PEAK"] else self.opt["PEAK"]
        self.parent.audivolnormalize = AudioVolNormal(title,
                                                      lev,
                                                      self.appdata['ostype'],
                                                      )
        self.parent.audivolnormalize.Show()
    # ------------------------------------------------------------------#

    def update_options(self):
        """
        Update entries.
        """
        if self.spin_Vbrate.IsEnabled() and not self.slider_CRF.IsEnabled():
            self.on_Vbitrate(self)

        elif self.slider_CRF.IsEnabled() and not self.spin_Vbrate.IsEnabled():
            self.on_Crf(self)

        elif self.slider_CRF.GetValue() == -1 and self.spin_Vbrate.IsEnabled():
            self.on_Vbitrate(self)

        elif self.slider_CRF.IsEnabled() and self.spin_Vbrate.IsEnabled():
            self.on_Vbitrate(self), self.on_Crf(self)

        else:
            self.opt["CRF"] = ''
            self.opt["VideoBitrate"] = ''

        if self.opt["VideoCodec"] not in ["-c:v libx264", "-c:v libx265",
                                          "-c:v libvpx", "-c:v libvpx-vp9",
                                          "-c:v libaom-av1"
                                          ]:
            self.opt["CpuUsed"], self.opt["Deadline"] = '', ''
            self.opt["RowMthreading"], self.opt["GOP"] = '', ''
            self.opt["Usage"], self.opt["Preset"] = '', ''
            self.opt["Profile"], self.opt["Level"] = '', ''
            self.opt["Tune"] = ''

        if self.spinMinr.GetValue() > -1:
            self.opt["MinRate"] = f'-minrate {self.spinMinr.GetValue()}k'
        else:
            self.opt["MinRate"] = ''
        if self.spinMaxr.GetValue() > -1:
            self.opt["MaxRate"] = f'-maxrate {self.spinMaxr.GetValue()}k'
        else:
            self.opt["MaxRate"] = ''
        if self.spinBufsize.GetValue() > -1:
            self.opt["Bufsize"] = f'-bufsize {self.spinBufsize.GetValue()}k'
        else:
            self.opt["Bufsize"] = ''

        if self.cmb_Pixfrm.GetValue() == 'None':
            self.opt["PixFmt"] = ''
        else:
            self.opt["PixFmt"] = f'-pix_fmt {self.cmb_Pixfrm.GetValue()}'

        smap = self.cmb_Submap.GetValue()
        if smap == 'None':
            self.opt["SubtitleMap"] = '-sn'
        elif smap == 'All':
            self.opt["SubtitleMap"] = '-map 0:s?'
    # ------------------------------------------------------------------#

    def on_start(self):
        """
        Check all settings before redirecting
        to the build command.

        """
        logname = 'AV_conversions.log'
        # check normalization data offset, if enable
        if self.rdbx_normalize.GetSelection() in [1, 2]:
            if self.btn_voldect.IsEnabled():
                wx.MessageBox(_('Undetected volume values! Click the '
                                '"Volume detect" button to analyze '
                                'audio volume data.'),
                              'Videomass', wx.ICON_INFORMATION, self)
                return

        self.update_options()  # update
        checking = check_files(self.parent.file_src,
                               self.parent.outputdir,
                               self.parent.same_destin,
                               self.parent.suffix,
                               self.opt["OutputFormat"],
                               self.parent.outputnames
                               )
        if not checking:  # User changing idea or not such files exist
            return

        f_src, f_dest = checking

        if self.cmb_Media.GetValue() == 'Video':  # CHECKING
            if self.rdbx_normalize.GetSelection() == 3:  # EBU
                self.video_ebu_2pass(f_src, f_dest, logname)
            elif self.opt["Vidstabdetect"]:
                self.video_stabilizer(f_src, f_dest, logname)
            else:
                self.video_stdProc(f_src, f_dest, logname)

        elif self.cmb_Media.GetValue() == 'Audio':  # CHECKING
            if self.rdbx_normalize.GetSelection() == 3:
                self.audio_ebu_2pass(f_src, f_dest, logname)
            else:
                self.audio_stdProc(f_src, f_dest, logname)
        return
    # ------------------------------------------------------------------#

    def video_stabilizer(self, f_src, f_dest, logname):
        """
        Build ffmpeg command strings for two pass
        video stabilizations process.

        """
        audnorm = self.opt["RMS"] if not self.opt["PEAK"] else self.opt["PEAK"]

        cmd1 = (f'-an -sn {self.opt["PixFmt"]} -vf '
                f'{self.opt["Vidstabdetect"]} -f null')
        cmd2 = (
            f'{self.opt["VideoCodec"]} {self.opt["VideoBitrate"]} '
            f'{self.opt["MinRate"]} {self.opt["MaxRate"]} '
            f'{self.opt["Bufsize"]} {self.opt["CRF"]} '
            f'{self.opt["Deadline"]} {self.opt["Usage"]}  '
            f'{self.opt["CpuUsed"]} {self.opt["RowMthreading"]}'
            f'{self.opt["GOP"]} {self.opt["Preset"]} '
            f'{self.opt["Profile"]} {self.opt["Level"]} '
            f'{self.opt["Tune"]} {self.opt["AspectRatio"]} '
            f'{self.opt["FPS"]} {self.opt["VFilters"]} '
            f'{self.opt["PixFmt"]} {self.opt["WebOptim"]} '
            f'-map 0:v? -map_chapters 0 '
            f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
            f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
            f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
            f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
            f'-map_metadata 0')

        pass1 = " ".join(cmd1.split())
        pass2 = " ".join(cmd2.split())

        if logname == 'save as profile':
            return pass1, pass2, self.opt["OutputFormat"]
        valupdate = self.update_dict(len(f_src), [''])
        ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                         self.parent.movetotrash, self.parent.emptylist,
                         )
        if ending.ShowModal() == wx.ID_OK:
            self.parent.movetotrash, self.parent.emptylist = ending.getvalue()
            self.parent.switch_to_processing('libvidstab',
                                             f_src,
                                             None,
                                             f_dest,
                                             self.opt["Makeduo"],
                                             [pass1, pass2],
                                             self.opt["VFilters"],
                                             [vol[5] for vol in audnorm],
                                             logname,
                                             len(f_src),
                                             )
        return None
        # ------------------------------------------------------------------#

    def video_stdProc(self, f_src, f_dest, logname):
        """
        Build the ffmpeg command strings for video conversions.
        """
        audnorm = self.opt["RMS"] if not self.opt["PEAK"] else self.opt["PEAK"]

        if self.cmb_Vcod.GetValue() == "Copy":
            command = (
                f'{self.opt["VideoCodec"]} {self.opt["PixFmt"]} '
                f'{self.opt["WebOptim"]} {self.opt["AspectRatio"]} '
                f'{self.opt["FPS"]}  -map 0:v? -map_chapters 0 '
                f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
                f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
                f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
                f'-map_metadata 0'
            )
            command = " ".join(command.split())  # mi formatta la stringa
            if logname == 'save as profile':
                return command, '', self.opt["OutputFormat"]
            valupdate = self.update_dict(len(f_src), ["Copy"])
            ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                             self.parent.movetotrash, self.parent.emptylist,
                             )
            if ending.ShowModal() == wx.ID_OK:
                end = ending.getvalue()
                self.parent.movetotrash, self.parent.emptylist = end[0], end[1]
                self.parent.switch_to_processing('onepass',
                                                 f_src,
                                                 None,
                                                 f_dest,
                                                 command,
                                                 None,
                                                 '',
                                                 [vol[5] for vol in audnorm],
                                                 logname,
                                                 len(f_src),
                                                 )
        elif self.opt["Passing"] == "2 pass":
            if self.opt["VideoCodec"] == "-c:v libx265":
                opt1, opt2 = '-x265-params pass=1', '-x265-params pass=2'
            else:
                opt1, opt2 = '-pass 1', '-pass 2'

            cmd1 = (f'-an -sn {self.opt["VideoCodec"]} '
                    f'{self.opt["VideoBitrate"]} {self.opt["MinRate"]} '
                    f'{self.opt["MaxRate"]} {self.opt["Bufsize"]} '
                    f'{self.opt["CRF"]} {self.opt["Deadline"]} '
                    f'{self.opt["Usage"]} {self.opt["CpuUsed"]} '
                    f'{self.opt["RowMthreading"]} {self.opt["GOP"]} '
                    f'{self.opt["Preset"]} {self.opt["Profile"]} '
                    f'{self.opt["Level"]} {self.opt["Tune"]} '
                    f'{self.opt["AspectRatio"]} {self.opt["FPS"]} '
                    f'{self.opt["VFilters"]} {self.opt["PixFmt"]} '
                    f'{self.opt["WebOptim"]} {opt1} -f rawvideo'
                    )
            cmd2 = (
                f'{self.opt["VideoCodec"]} {self.opt["VideoBitrate"]} '
                f'{self.opt["MinRate"]} {self.opt["MaxRate"]} '
                f'{self.opt["Bufsize"]} {self.opt["CRF"]} '
                f'{self.opt["Deadline"]} {self.opt["Usage"]} '
                f'{self.opt["CpuUsed"]} {self.opt["RowMthreading"]} '
                f'{self.opt["GOP"]} {self.opt["Profile"]} {self.opt["Level"]} '
                f'{self.opt["Tune"]} {self.opt["AspectRatio"]} '
                f'{self.opt["FPS"]} {self.opt["VFilters"]} '
                f'{self.opt["PixFmt"]} {self.opt["WebOptim"]} '
                f'-map 0:v? -map_chapters 0 {opt2} '
                f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
                f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
                f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
                f'-map_metadata 0'
            )
            pass1 = " ".join(cmd1.split())
            pass2 = " ".join(cmd2.split())
            if logname == 'save as profile':
                return pass1, pass2, self.opt["OutputFormat"]
            valupdate = self.update_dict(len(f_src), [''])
            ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                             self.parent.movetotrash, self.parent.emptylist,
                             )
            if ending.ShowModal() == wx.ID_OK:
                end = ending.getvalue()
                self.parent.movetotrash, self.parent.emptylist = end[0], end[1]
                self.parent.switch_to_processing('twopass',
                                                 f_src,
                                                 None,
                                                 f_dest,
                                                 None,
                                                 [pass1, pass2],
                                                 '',
                                                 [vol[5] for vol in audnorm],
                                                 logname,
                                                 len(f_src),
                                                 )
        elif self.opt["Passing"] == "1 pass":  # Batch-Mode / h264 Codec
            command = (
                f'{self.opt["VideoCodec"]} {self.opt["VideoBitrate"]} '
                f'{self.opt["MinRate"]} {self.opt["MaxRate"]} '
                f'{self.opt["Bufsize"]} {self.opt["CRF"]} '
                f'{self.opt["Deadline"]} {self.opt["Usage"]} '
                f'{self.opt["CpuUsed"]} {self.opt["RowMthreading"]} '
                f'{self.opt["GOP"]} {self.opt["Preset"]} '
                f'{self.opt["Profile"]} {self.opt["Level"]} '
                f'{self.opt["Tune"]} {self.opt["AspectRatio"]} '
                f'{self.opt["FPS"]} {self.opt["VFilters"]} '
                f'{self.opt["PixFmt"]} {self.opt["WebOptim"]} '
                f'-map 0:v? -map_chapters 0 '
                f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
                f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
                f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
                f'-map_metadata 0'
            )
            command = " ".join(command.split())  # mi formatta la stringa
            if logname == 'save as profile':
                return command, '', self.opt["OutputFormat"]
            valupdate = self.update_dict(len(f_src), [''])
            ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                             self.parent.movetotrash, self.parent.emptylist,
                             )
            if ending.ShowModal() == wx.ID_OK:
                end = ending.getvalue()
                self.parent.movetotrash, self.parent.emptylist = end[0], end[1]
                self.parent.switch_to_processing('onepass',
                                                 f_src,
                                                 self.opt["OutputFormat"],
                                                 f_dest,
                                                 command,
                                                 None,
                                                 '',
                                                 [vol[5] for vol in audnorm],
                                                 logname,
                                                 len(f_src),
                                                 )
        return None
    # ------------------------------------------------------------------#

    def video_ebu_2pass(self, f_src, f_dest, logname):
        """
        Define the ffmpeg command strings for batch process with
        EBU two-passes conversion.
        NOTE If you want leave same indexes and process a selected Input Audio
             Index use same Output Audio Index on Audio Streams Mapping box

        """
        self.opt["EBU"] = 'EBU R128'
        loudfilter = (f'loudnorm=I={str(self.spin_i.GetValue())}:'
                      f'TP={str(self.spin_tp.GetValue())}:'
                      f'LRA={str(self.spin_lra.GetValue())}:'
                      f'print_format=summary'
                      )
        if self.opt["VideoCodec"] == "-c:v libx265":
            opt1, opt2 = '-x265-params pass=1', '-x265-params pass=2'
        else:
            opt1, opt2 = '-pass 1', '-pass 2'

        if self.cmb_Vcod.GetValue() == "Copy":
            cmd_1 = (f'-map 0:v? {self.opt["AudioIndex"]} '
                     f'-filter:a: {loudfilter} '
                     f'-vn -sn {opt1} {self.opt["AspectRatio"]} '
                     f'{self.opt["FPS"]} -f null'
                     )
            cmd_2 = (
                f'{self.opt["VideoCodec"]} {opt2} {self.opt["AspectRatio"]} '
                f'{self.opt["FPS"]} {self.opt["PixFmt"]} '
                f'{self.opt["WebOptim"]} -map 0:v? -map_chapters 0 '
                f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
                f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
                f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
                f'-map_metadata 0'
            )
            pass1 = " ".join(cmd_1.split())
            pass2 = " ".join(cmd_2.split())
            if logname == 'save as profile':
                return pass1, pass2, self.opt["OutputFormat"]
            valupdate = self.update_dict(len(f_src), ["Copy"])
            ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                             self.parent.movetotrash, self.parent.emptylist,
                             )
            if ending.ShowModal() == wx.ID_OK:
                end = ending.getvalue()
                self.parent.movetotrash, self.parent.emptylist = end[0], end[1]
                self.parent.switch_to_processing('two pass EBU',
                                                 f_src,
                                                 None,
                                                 f_dest,
                                                 None,
                                                 [pass1, pass2, loudfilter],
                                                 self.opt["AudioMap"],
                                                 None,
                                                 logname,
                                                 len(f_src),
                                                 )
        else:
            cmd_1 = (f'{self.opt["VideoCodec"]} {self.opt["VideoBitrate"]} '
                     f'{self.opt["MinRate"]} {self.opt["MaxRate"]} '
                     f'{self.opt["Bufsize"]} {self.opt["CRF"]} '
                     f'{self.opt["Deadline"]} {self.opt["Usage"]} '
                     f'{self.opt["CpuUsed"]} {self.opt["RowMthreading"]} '
                     f'{self.opt["GOP"]} {self.opt["Preset"]} '
                     f'{self.opt["Profile"]} {self.opt["Level"]} '
                     f'{self.opt["Tune"]} {self.opt["AspectRatio"]} '
                     f'{self.opt["FPS"]} {self.opt["VFilters"]} '
                     f'{self.opt["PixFmt"]} {self.opt["WebOptim"]} '
                     f'-map 0:v? {self.opt["AudioIndex"]}  '
                     f'{opt1} -sn -filter:a: {loudfilter} '
                     f'-f {AV_Conv.MUXERS[self.opt["OutputFormat"]]}'
                     )
            cmd_2 = (
                f'{self.opt["VideoCodec"]} {self.opt["VideoBitrate"]} '
                f'{self.opt["MinRate"]} {self.opt["MaxRate"]} '
                f'{self.opt["Bufsize"]} {self.opt["CRF"]} '
                f'{self.opt["Deadline"]} {self.opt["Usage"]} '
                f'{self.opt["CpuUsed"]} {self.opt["RowMthreading"]} '
                f'{self.opt["GOP"]} {self.opt["Preset"]} '
                f'{self.opt["Profile"]} {self.opt["Level"]} '
                f'{self.opt["Tune"]} {self.opt["AspectRatio"]} '
                f'{self.opt["FPS"]} {self.opt["VFilters"]} '
                f'{self.opt["PixFmt"]} {self.opt["WebOptim"]} '
                f'-map 0:v? -map_chapters 0 {opt2} '
                f'{self.opt["SubtitleMap"]} {self.opt["AudioCodec"][0]} '
                f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
                f'{self.opt["AudioDepth"][1]} {self.opt["AudioMap"][0]} '
                f'-map_metadata 0'
            )
            pass1 = " ".join(cmd_1.split())
            pass2 = " ".join(cmd_2.split())  # mi formatta la stringa
            if logname == 'save as profile':
                return pass1, pass2, self.opt["OutputFormat"]
            valupdate = self.update_dict(len(f_src), [''])
            ending = Formula(self, valupdate[0], valupdate[1], (600, 400),
                             self.parent.movetotrash, self.parent.emptylist,
                             )
            if ending.ShowModal() == wx.ID_OK:
                end = ending.getvalue()
                self.parent.movetotrash, self.parent.emptylist = end[0], end[1]
                self.parent.switch_to_processing('two pass EBU',
                                                 f_src,
                                                 self.opt["OutputFormat"],
                                                 f_dest,
                                                 None,
                                                 [pass1, pass2, loudfilter],
                                                 self.opt["AudioMap"],
                                                 None,
                                                 logname,
                                                 len(f_src),
                                                 )
            # ending.Destroy() # con ID_OK e ID_CANCEL non serve Destroy()
        return None
    # ------------------------------------------------------------------#

    def audio_stdProc(self, f_src, f_dest, logname):
        """
        Build the ffmpeg command strings for audio conversion.

        """
        audnorm = self.opt["RMS"] if not self.opt["PEAK"] else self.opt["PEAK"]
        command = (
            f'-vn -sn {self.opt["WebOptim"]} {self.opt["AudioMap"][0]} '
            f'{self.opt["AudioCodec"][0]} {self.opt["AudioCodec"][1]} '
            f'{self.opt["AudioBitrate"][1]} {self.opt["AudioDepth"][1]} '
            f'{self.opt["AudioRate"][1]} {self.opt["AudioChannel"][1]} '
            f'-map_metadata 0'
        )
        command = " ".join(command.split())  # mi formatta la stringa
        if logname == 'save as profile':
            return command, '', self.opt["OutputFormat"]
        valupdate = self.update_dict(len(f_src), [''])
        ending = Formula(self, valupdate[0], valupdate[1], (600, 280),
                         self.parent.movetotrash, self.parent.emptylist,
                         )

        if ending.ShowModal() == wx.ID_OK:
            self.parent.movetotrash, self.parent.emptylist = ending.getvalue()
            self.parent.switch_to_processing('onepass',
                                             f_src,
                                             self.opt["OutputFormat"],
                                             f_dest,
                                             command,
                                             None,
                                             '',
                                             [vol[5] for vol in audnorm],
                                             logname,
                                             len(f_src),
                                             )
        return None
    # ------------------------------------------------------------------#

    def audio_ebu_2pass(self, f_src, f_dest, logname):
        """
        Perform EBU R128 normalization on audio conversion
        WARNING do not map output audio file index on filter:a: , -c:a:
        and not send self.opt["AudioMap"] to process because the files
        audio has not indexes
        """
        self.opt["EBU"] = True

        loudfilter = (f'loudnorm=I={str(self.spin_i.GetValue())}:'
                      f'TP={str(self.spin_tp.GetValue())}:'
                      f'LRA={str(self.spin_lra.GetValue())}:'
                      f'print_format=summary'
                      )
        cmd_1 = (f'{self.opt["WebOptim"]} {self.opt["AudioMap"][0]} '
                 f'-filter:a: {loudfilter} -vn -sn -pass 1 -f null'
                 )
        cmd_2 = (f'-vn -sn {self.opt["WebOptim"]} {self.opt["AudioMap"][0]} '
                 f'-pass 2 {self.opt["AudioCodec"][0]} '
                 f'{self.opt["AudioCodec"][1]} {self.opt["AudioBitrate"][1]} '
                 f'{self.opt["AudioDepth"][1]} {self.opt["AudioRate"][1]} '
                 f'{self.opt["AudioChannel"][1]} -map_metadata 0'
                 )
        pass1 = " ".join(cmd_1.split())
        pass2 = " ".join(cmd_2.split())
        if logname == 'save as profile':
            return pass1, pass2, self.opt["OutputFormat"]
        valupdate = self.update_dict(len(f_src), [''])
        ending = Formula(self, valupdate[0], valupdate[1], (600, 280),
                         self.parent.movetotrash, self.parent.emptylist,
                         )

        if ending.ShowModal() == wx.ID_OK:
            self.parent.movetotrash, self.parent.emptylist = ending.getvalue()
            self.parent.switch_to_processing('two pass EBU',
                                             f_src,
                                             self.opt["OutputFormat"],
                                             f_dest,
                                             None,
                                             [pass1, pass2, loudfilter],
                                             ['', ''],  # do not map audio file
                                             None,
                                             logname,
                                             len(f_src),
                                             )
        return None
    # ------------------------------------------------------------------#

    def update_dict(self, countmax, prof):
        """
        Update all settings before send to epilogue
        """
        numfile = _("{} file in queue").format(str(countmax))
        if self.opt["PEAK"]:
            normalize = 'PEAK'
        elif self.opt["RMS"]:
            normalize = 'RMS'
        elif self.opt["EBU"]:
            normalize = 'EBU R128'
        else:
            normalize = _('Off')
        if self.cmb_Vcont.GetValue() == "Copy":
            outputformat = "Copy"
        else:
            outputformat = self.opt["OutputFormat"]
        if not self.parent.time_seq:
            time = _('Unset')
        else:
            t = self.parent.time_seq.split()
            time = _('start  {} | duration  {}').format(t[1], t[3])

        vfilter = _('Enabled') if self.opt["VFilters"] else _('Disabled')

        # ------------------
        if self.cmb_Media.GetValue() == 'Audio':
            formula = (_("Queued File\nOutput Format"
                         "\nWeb Optimize\nAudio Codec\nAudio bit-rate"
                         "\nAudio Channels\nAudio Rate\nBit per Sample"
                         "\nAudio Normalization\nTime Period"
                         "\nInput Audio Map"
                         ))
            dictions = (f'{numfile}\n{outputformat}\n'
                        f'{self.opt["WebOptim"]}\n'
                        f'{self.opt["AudioCodStr"]}\n'
                        f'{self.opt["AudioBitrate"][0]}\n'
                        f'{self.opt["AudioChannel"][0]}\n'
                        f'{self.opt["AudioRate"][0]}\n'
                        f'{self.opt["AudioDepth"][0]}\n{normalize}\n{time}\n'
                        f'{self.cmb_A_outMap.GetValue()}'
                        )
        elif prof[0] == "Copy":
            formula = (_("Queued File\nWeb Optimize\nOutput Format"
                         "\nVideo Codec\nAspect Ratio\nFPS\nAudio Codec"
                         "\nAudio Channels\nAudio Rate\nAudio bit-rate"
                         "\nBit per Sample\nAudio Normalization"
                         "\nInput Audio Map\nOutput Audio Map"
                         "\nSubtitles Map\nTime Period"
                         ))
            dictions = (f'{numfile}\n{self.opt["WebOptim"]}\n'
                        f'{outputformat}\n{self.opt["VidCmbxStr"]}\n'
                        f'{self.opt["AspectRatio"]}\n{self.opt["FPS"]}\n'
                        f'{self.opt["AudioCodStr"]}\n'
                        f'{self.opt["AudioChannel"][0]}\n'
                        f'{self.opt["AudioRate"][0]}\n'
                        f'{self.opt["AudioBitrate"][0]}\n'
                        f'{self.opt["AudioDepth"][0]}\n{normalize}\n'
                        f'{self.cmb_A_inMap.GetValue()}\n'
                        f'{self.cmb_A_outMap.GetValue()}\n'
                        f'{self.cmb_Submap.GetValue()}\n{time}'
                        )
        # --------------------
        else:
            formula = (_("Queued File\nWeb Optimize\nPass Encoding"
                         "\nOutput Format\nVideo Codec\nVideo bit-rate"
                         "\nCRF\nMin Rate\nMax Rate\nBuffer size"
                         "\nEnabled Options\nVideo Filters\nAspect Ratio\nFPS"
                         "\nPreset\nProfile\nTune\nAudio Codec"
                         "\nAudio Channels\nAudio Rate\nAudio bit-rate"
                         "\nBit per Sample\nAudio Normalization"
                         "\nInput Audio Map\nOutput Audio Map"
                         "\nSubtitles Map\nTime Period"
                         ))
            dictions = (f'{numfile}\n{self.opt["WebOptim"]}\n'
                        f'{self.opt["Passing"]}\n{outputformat}\n'
                        f'{self.opt["VidCmbxStr"]}\n'
                        f'{self.opt["VideoBitrate"]}\n{self.opt["CRF"]}\n'
                        f'{self.opt["MinRate"]}\n{self.opt["MaxRate"]}\n'
                        f'{self.opt["Bufsize"]}\n{self.opt["Deadline"]} '
                        f'{self.opt["Usage"]} {self.opt["CpuUsed"]} '
                        f'{self.opt["RowMthreading"]} {self.opt["GOP"]}\n'
                        f'{vfilter}\n{self.opt["AspectRatio"]}\n'
                        f'{self.opt["FPS"]}\n{self.opt["Preset"]}\n'
                        f'{self.opt["Profile"]} {self.opt["Level"]}\n'
                        f'{self.opt["Tune"]}\n{self.opt["AudioCodStr"]}\n'
                        f'{self.opt["AudioChannel"][0]}\n'
                        f'{self.opt["AudioRate"][0]}\n'
                        f'{self.opt["AudioBitrate"][0]}\n'
                        f'{self.opt["AudioDepth"][0]}\n{normalize}\n'
                        f'{self.cmb_A_inMap.GetValue()}\n'
                        f'{self.cmb_A_outMap.GetValue()}\n'
                        f'{self.cmb_Submap.GetValue()}\n{time}'
                        )
        return formula, dictions
# ------------------------------------------------------------------#

    def on_saveprst(self, event):
        """
        Save current setting as profile for the Presets
        Manager panel
        """
        if self.rdbx_normalize.GetSelection() in (1, 2, 3):  # EBU
            if wx.MessageBox(_('Audio normalization data cannot be saved '
                               'on the Presets Manager.\n\n'
                               'Do you want to continue?'),
                             'Videomass', wx.ICON_QUESTION
                             | wx.CANCEL | wx.YES_NO, self) != wx.YES:
                return

        self.update_options()
        if self.cmb_Media.GetValue() == 'Video':
            if self.opt["Vidstabdetect"]:
                parameters = self.video_stabilizer([], [], 'save as profile')
            else:
                parameters = self.video_stdProc([], [], 'save as profile')

        elif self.cmb_Media.GetValue() == 'Audio':
            parameters = self.audio_stdProc([], [], 'save as profile')

        with wx.FileDialog(
                None, _("Choose a Videomass preset..."),
                defaultDir=os.path.join(self.appdata['confdir'], 'presets'),
                wildcard="Videomass presets (*.json;)|*.json;",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            filename = os.path.splitext(fileDialog.GetPath())[0]

            title = _('Create a new profile')

        with presets_addnew.MemPresets(self, 'addprofile',
                                       os.path.basename(filename),
                                       parameters,
                                       title,
                                       ) as prstdialog:

            if prstdialog.ShowModal() == wx.ID_CANCEL:
                return
        self.parent.PrstsPanel.presets_refresh(self)
