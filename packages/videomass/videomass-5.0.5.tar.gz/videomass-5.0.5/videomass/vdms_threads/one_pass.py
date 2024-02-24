# -*- coding: UTF-8 -*-
"""
Name: one_pass.py
Porpose: FFmpeg long processing task for one pass processing
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


class OnePass(Thread):
    """
    This class represents a separate thread for running processes,
    which need to read the stdout/stderr in real time.

    capturing output in real-time (Windows, Unix):
    https://stackoverflow.com/questions/1388753/how-to-get-output-
    from-subprocess-popen-proc-stdout-readline-blocks-no-dat?rq=1
    """
    get = wx.GetApp()  # get videomass wx.App attributes
    appdata = get.appset
    NOT_EXIST_MSG = _("Is 'ffmpeg' installed on your system?")
    # ---------------------------------------------------------------

    def __init__(self, logname, duration, timeseq, *args):
        """
        Called from `long_processing_task.topic_thread`.
        Also see `main_frame.switch_to_processing`.
        """
        self.stop_work_thread = False  # process terminate
        self.input_flist = args[1]  # list of infile (items)
        self.command = args[4]  # comand set on single pass
        self.output_flist = args[3]  # output path
        self.duration = duration  # duration list
        self.volume = args[7]  # (lista norm.)se non richiesto rimane None
        self.count = 0  # count first for loop
        self.countmax = len(args[1])  # length file list
        self.logname = logname  # title name of file log
        self.timeseq = timeseq  # ss, t tuple

        Thread.__init__(self)

        self.start()  # start the thread

    def run(self):
        """
        Thread started.
        """
        filedone = []
        for (infile,
             outfile,
             volume,
             duration) in itertools.zip_longest(self.input_flist,
                                                self.output_flist,
                                                self.volume,
                                                self.duration,
                                                fillvalue='',
                                                ):
            cmd = (f'"{OnePass.appdata["ffmpeg_cmd"]}" '
                   f'{self.timeseq[0]} '
                   f'{OnePass.appdata["ffmpeg_default_args"]} '
                   f'-i "{infile}" '
                   f'{self.timeseq[1]} '
                   f'{self.command} '
                   f'{volume} '
                   f'{OnePass.appdata["ffthreads"]} '
                   f'-y "{outfile}"'
                   )
            self.count += 1
            count = f'File {self.count}/{self.countmax}'
            com = (f'{count}\nSource: "{infile}"\nDestination: "{outfile}"'
                   f'\n\n[COMMAND]:\n{cmd}')

            wx.CallAfter(pub.sendMessage,
                         "COUNT_EVT",
                         count=count,
                         fsource=f'Source:  "{infile}"',
                         destination=f'Destination:  "{outfile}"',
                         duration=duration,
                         end='',
                         )
            logwrite(com, '', self.logname)  # write n/n + command only

            if not platform.system() == 'Windows':
                cmd = shlex.split(cmd)

            try:
                with Popen(cmd,
                           stderr=subprocess.PIPE,
                           bufsize=1,
                           universal_newlines=True,
                           encoding='utf8',
                           ) as proc:
                    for line in proc.stderr:
                        wx.CallAfter(pub.sendMessage,
                                     "UPDATE_EVT",
                                     output=line,
                                     duration=duration,
                                     status=0,
                                     )
                        if self.stop_work_thread:
                            proc.terminate()
                            break  # break second 'for' loop

                    if proc.wait():  # error
                        wx.CallAfter(pub.sendMessage,
                                     "UPDATE_EVT",
                                     output='',
                                     duration=duration,
                                     status=proc.wait(),
                                     )
                        logwrite('',
                                 f"Exit status: {proc.wait()}",
                                 self.logname,
                                 )  # append exit error number
                    else:  # ok
                        filedone.append(infile)
                        wx.CallAfter(pub.sendMessage,
                                     "COUNT_EVT",
                                     count='',
                                     fsource='',
                                     destination='',
                                     duration=duration,
                                     end='Done'
                                     )
            except (OSError, FileNotFoundError) as err:
                excepterr = f"{err}\n  {OnePass.NOT_EXIST_MSG}"
                wx.CallAfter(pub.sendMessage,
                             "COUNT_EVT",
                             count=excepterr,
                             fsource='',
                             destination='',
                             duration=0,
                             end='error',
                             )
                break

            if self.stop_work_thread:
                proc.terminate()
                break  # break second 'for' loop

        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "END_EVT", msg=filedone)
    # --------------------------------------------------------------------#

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
