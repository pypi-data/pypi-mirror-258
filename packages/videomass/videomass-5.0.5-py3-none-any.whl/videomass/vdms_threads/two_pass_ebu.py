# -*- coding: UTF-8 -*-
"""
Name: two_pass_EBU.py
Porpose: FFmpeg long processing task with EBU normalization
Compatibility: Python3, wxPython4 Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyleft - 2024 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.17.2024
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
from threading import Thread
import time
import itertools
import subprocess
import platform
import wx
from pubsub import pub
from videomass.vdms_utils.utils import Popen
from videomass.vdms_io.make_filelog import logwrite
if not platform.system() == 'Windows':
    import shlex


class Loudnorm(Thread):
    """
    Like `TwoPass_Thread` but execute -loudnorm parsing from first
    pass and has definitions to apply on second pass.

    NOTE capturing output in real-time (Windows, Unix):

    https://stackoverflow.com/questions/1388753/how-to-get-output-
    from-subprocess-popen-proc-stdout-readline-blocks-no-dat?rq=1

    """
    get = wx.GetApp()  # get videomass wx.App attribute
    appdata = get.appset
    OS = appdata['ostype']
    NOT_EXIST_MSG = _("Is 'ffmpeg' installed on your system?")

    def __init__(self, logname, duration, timeseq, *args):
        """
        Called from `long_processing_task.topic_thread`.
        Also see `main_frame.switch_to_processing`.
        """
        self.stop_work_thread = False  # process terminate
        self.input_flist = args[1]  # list of infile (elements)
        self.passlist = args[5]  # comand list
        self.audio_outmap = args[6]  # map output list
        self.output_flist = args[3]  # output path
        self.duration = duration  # durations list
        self.time_seq = timeseq  # time segments list
        self.count = 0  # count first for loop
        self.countmax = len(args[1])  # length file list
        self.logname = logname  # title name of file log
        self.nul = 'NUL' if Loudnorm.OS == 'Windows' else '/dev/null'

        Thread.__init__(self)
        self.start()  # start the thread (va in self.run())

    def run(self):
        """
        Subprocess initialize thread.
        """
        filedone = []
        summary = {'Input Integrated:': None, 'Input True Peak:': None,
                   'Input LRA:': None, 'Input Threshold:': None,
                   'Output Integrated:': None, 'Output True Peak:': None,
                   'Output LRA:': None, 'Output Threshold:': None,
                   'Normalization Type:': None, 'Target Offset:': None
                   }
        for (infile,
             outfile,
             duration) in itertools.zip_longest(self.input_flist,
                                                self.output_flist,
                                                self.duration,
                                                fillvalue='',
                                                ):
            # --------------- first pass
            pass1 = (f'"{Loudnorm.appdata["ffmpeg_cmd"]}" '
                     f'{Loudnorm.appdata["ffmpeg_default_args"]} '
                     f'{self.time_seq[0]} '
                     f'-i "{infile}" '
                     f'{self.time_seq[1]} '
                     f'{self.passlist[0]} '
                     f'{Loudnorm.appdata["ffthreads"]} '
                     f'-y {self.nul}'
                     )
            self.count += 1
            count = (f'File {self.count}/{self.countmax} - Pass One\n '
                     f'Loudnorm ebu: Getting statistics for measurements...')
            cmd = (f'{count}\nSource: "{infile}"\nDestination: '
                   f'"{self.nul}"\n\n'
                   f'[COMMAND]:\n{pass1}')

            wx.CallAfter(pub.sendMessage,
                         "COUNT_EVT",
                         count=count,
                         fsource=f'Source:  "{infile}"',
                         destination=f'Destination: "{self.nul}"',
                         duration=duration,
                         end='',
                         )
            logwrite(cmd, '', self.logname)  # write n/n + command only

            if not Loudnorm.OS == 'Windows':
                pass1 = shlex.split(pass1)
            try:
                with Popen(pass1,
                           stderr=subprocess.PIPE,
                           bufsize=1,
                           universal_newlines=True,
                           encoding='utf8',
                           ) as proc1:

                    for line in proc1.stderr:
                        wx.CallAfter(pub.sendMessage,
                                     "UPDATE_EVT",
                                     output=line,
                                     duration=duration,
                                     status=0
                                     )
                        if self.stop_work_thread:  # break first 'for' loop
                            proc1.terminate()
                            break

                        for k in summary:
                            if line.startswith(k):
                                summary[k] = line.split(':')[1].split()[0]

                    if proc1.wait():  # will add '..failed' to txtctrl
                        wx.CallAfter(pub.sendMessage,
                                     "UPDATE_EVT",
                                     output='',
                                     duration=duration,
                                     status=proc1.wait(),
                                     )
                        logwrite('',
                                 f"Exit status: {proc1.wait()}",
                                 self.logname,
                                 )  # append exit error number
                        break

            except (OSError, FileNotFoundError) as err:
                excepterr = f"{err}\n  {Loudnorm.NOT_EXIST_MSG}"
                wx.CallAfter(pub.sendMessage,
                             "COUNT_EVT",
                             count=excepterr,
                             fsource='',
                             destination='',
                             duration=0,
                             end='error'
                             )
                break

            if self.stop_work_thread:  # break first 'for' loop
                proc1.terminate()
                break  # fermo il ciclo for, altrimenti passa avanti

            if proc1.wait() == 0:  # will add '..terminated' to txtctrl
                wx.CallAfter(pub.sendMessage,
                             "COUNT_EVT",
                             count='',
                             fsource='',
                             destination='',
                             duration=duration,
                             end='Done'
                             )
            # --------------- second pass ----------------#
            filters = (f'{self.passlist[2]}'
                       f':measured_I={summary["Input Integrated:"]}'
                       f':measured_LRA={summary["Input LRA:"]}'
                       f':measured_TP={summary["Input True Peak:"]}'
                       f':measured_thresh={summary["Input Threshold:"]}'
                       f':offset={summary["Target Offset:"]}'
                       f':linear=true:dual_mono=true'
                       )
            time.sleep(.5)

            pass2 = (f'"{Loudnorm.appdata["ffmpeg_cmd"]}" '
                     f'{Loudnorm.appdata["ffmpeg_default_args"]} '
                     f'{self.time_seq[0]} '
                     f'-i "{infile}" '
                     f'{self.time_seq[1]} '
                     f'{self.passlist[1]} '
                     f'-filter:a:{self.audio_outmap[1]} '
                     f'{filters} '
                     f'{Loudnorm.appdata["ffthreads"]} '
                     f'-y "{outfile}"'
                     )
            count = (f'File {self.count}/{self.countmax} - Pass Two\n'
                     f'Loudnorm ebu: apply EBU R128...'
                     )
            cmd = (f'\n{count}\nSource: "{infile}"\n'
                   f'Destination: "{outfile}"\n\n'
                   f'[COMMAND]:\n{pass2}'
                   )

            wx.CallAfter(pub.sendMessage,
                         "COUNT_EVT",
                         count=count,
                         fsource=f'Source:  "{infile}"',
                         destination=f'Destination: "{outfile}"',
                         duration=duration,
                         end='',
                         )
            logwrite(cmd, '', self.logname)

            if not Loudnorm.OS == 'Windows':
                pass2 = shlex.split(pass2)
            with Popen(pass2,
                       stderr=subprocess.PIPE,
                       bufsize=1,
                       universal_newlines=True,
                       encoding='utf8',
                       ) as proc2:

                for line2 in proc2.stderr:
                    wx.CallAfter(pub.sendMessage,
                                 "UPDATE_EVT",
                                 output=line2,
                                 duration=duration,
                                 status=0,
                                 )
                    if self.stop_work_thread:  # break first 'for' loop
                        proc2.terminate()
                        break

                if proc2.wait():  # will add '..failed' to txtctrl
                    wx.CallAfter(pub.sendMessage,
                                 "UPDATE_EVT",
                                 output='',
                                 duration=duration,
                                 status=proc2.wait(),
                                 )
                    logwrite('',
                             f"Exit status: {proc2.wait()}",
                             self.logname,
                             )  # append exit error number

            if self.stop_work_thread:  # break first 'for' loop
                proc2.terminate()
                break  # fermo il ciclo for, altrimenti passa avanti

            if proc2.wait() == 0:  # will add '..terminated' to txtctrl
                filedone.append(infile)
                wx.CallAfter(pub.sendMessage,
                             "COUNT_EVT",
                             count='',
                             fsource='',
                             destination='',
                             duration=duration,
                             end='Done'
                             )
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "END_EVT", msg=filedone)
    # --------------------------------------------------------------------#

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
